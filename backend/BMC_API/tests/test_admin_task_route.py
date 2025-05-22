# backend/BMC_API/tests/test_admin_task_route.py
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from BMC_API.src.application.use_cases.challenge_use_cases import ChallengeService
from BMC_API.src.application.use_cases.task_use_cases import TaskService

pytest_plugins = [
    "BMC_API.tests.fixtures.admin_user_fixtures",
    "BMC_API.tests.fixtures.user_fixtures",
]

CHALLENGE_ID = 1


@pytest.fixture
def patch_challenge_and_conference_open():
    # Mock task
    mock_conference = MagicMock(is_open_for_submissions=True)
    mock_challenge = MagicMock(challenge_conference=mock_conference, challenge_status="DRAFT")
    mock_task = MagicMock(task_challenge=mock_challenge, task_status="DRAFT")

    with (
        patch.object(TaskService, "get_raw", new=AsyncMock(return_value=mock_task)),
        patch.object(ChallengeService, "get_raw", new=AsyncMock(return_value=mock_challenge)),
    ):
        yield


@pytest.mark.anyio
class TestAdminTaskRoutes:
    async def test_admin_can_create_task_with_extra_control(
        self, client: AsyncClient, fastapi_app: FastAPI, admin_token
    ):
        task_data = {
            "task_name": "Test Task",
            "task_abstract": "This is a task for testing.",
            "task_locked": False,
            "task_owner_id": 3,
        }

        url = fastapi_app.url_path_for("create_task_route_admin")
        response = await client.post(
            f"{url}?challenge_id={CHALLENGE_ID}", json=task_data, headers={"Authorization": f"Bearer {admin_token}"}
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["task_name"] == task_data["task_name"]

    async def test_admin_can_access_other_users_task(
        self,
        client: AsyncClient,
        test_user: dict,
        test_admin_login,
        fastapi_app: FastAPI,
        user_token,
        admin_token,
    ):
        task_data = {
            "task_name": "UserTask",
            "task_abstract": "Owned by user",
        }

        create_url = fastapi_app.url_path_for("create_task_route")

        # Mock task only for creation process
        mock_conference = MagicMock(is_open_for_submissions=True)
        mock_challenge = MagicMock(challenge_conference=mock_conference)
        mock_task = MagicMock(task_challenge=mock_challenge)

        with (
            patch.object(TaskService, "get_raw", new=AsyncMock(return_value=mock_task)),
            patch.object(ChallengeService, "get_raw", new=AsyncMock(return_value=mock_challenge)),
        ):
            create_resp = await client.post(
                f"{create_url}?challenge_id={CHALLENGE_ID}",
                json=task_data,
                headers={"Authorization": f"Bearer {user_token}"},
            )

            task_id = create_resp.json()["id"]

        # Continue without any mocking
        # Admin tries to get the task
        get_url = fastapi_app.url_path_for("get_task_route_admin", id=task_id)
        response = await client.get(get_url, headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["task_name"] == task_data["task_name"]
        assert response.json()["task_abstract"] == task_data["task_abstract"]

    async def test_admin_can_get_all_tasks(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, admin_token, patch_challenge_and_conference_open
    ):
        # First create tasks
        data = {
            "task_name": "Bulk 1",
            "task_abstract": "Abstract",
        }
        create_url = fastapi_app.url_path_for("create_task_route")
        response = await client.post(
            f"{create_url}?challenge_id={CHALLENGE_ID}", json=data, headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_201_CREATED

        data["task_name"] = "Bulk 2"
        response = await client.post(
            f"{create_url}?challenge_id={CHALLENGE_ID}", json=data, headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_201_CREATED

        get_url = fastapi_app.url_path_for("list_tasks_route_admin")
        response = await client.post(get_url, headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["total_pages"] == 1
        assert response.json()["total_records"] == 2
        assert len(response.json()["content"]) == 2
        assert response.json()["content"][0]["task_name"] == "Bulk 1"
        assert response.json()["content"][1]["task_name"] == "Bulk 2"

    async def test_admin_can_update_other_users_task(
        self,
        client: AsyncClient,
        test_user: dict,
        test_admin_login,
        fastapi_app: FastAPI,
        user_token,
        admin_token,
        patch_challenge_and_conference_open,
    ):
        task_data = {
            "task_name": "User Owned",
            "task_abstract": "Should be protected",
        }

        create_url = fastapi_app.url_path_for("create_task_route")
        create_resp = await client.post(
            f"{create_url}?challenge_id={CHALLENGE_ID}",
            json=task_data,
            headers={"Authorization": f"Bearer {user_token}"},
        )
        task_id = create_resp.json()["id"]

        update_data = {
            "task_name": "Admin Attempt",
            "task_abstract": "Forbidden Update",
        }

        update_url = fastapi_app.url_path_for("update_task_route_admin", id=task_id)
        response = await client.put(update_url, json=update_data, headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["task_name"] == update_data["task_name"]
        assert response.json()["task_abstract"] == update_data["task_abstract"]

    async def test_admin_can_bulk_update_other_users_task(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, admin_token, patch_challenge_and_conference_open
    ):
        data = {
            "task_name": "Bulk 1",
            "task_abstract": "Abstract",
        }
        create_url = fastapi_app.url_path_for("create_task_route")
        resp1 = await client.post(
            f"{create_url}?challenge_id={CHALLENGE_ID}", json=data, headers={"Authorization": f"Bearer {user_token}"}
        )
        conf_id1 = resp1.json()["id"]

        data["task_name"] = "Bulk 2"
        resp2 = await client.post(
            f"{create_url}?challenge_id={CHALLENGE_ID}", json=data, headers={"Authorization": f"Bearer {user_token}"}
        )
        conf_id2 = resp2.json()["id"]

        bulk_update_url = fastapi_app.url_path_for("bulk_update_tasks_route_admin")
        updates = [
            {"id": conf_id1, "venue": "On-site"},
            {"id": conf_id2, "venue": "Remote"},
        ]

        response = await client.put(bulk_update_url, json=updates, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == status.HTTP_200_OK
        assert "Bulk update completed" in response.json()["detail"]
        assert len(response.json()["successful"]) == 2
        assert response.json()["successful"][0]["task_name"] == "Bulk 1"
        assert response.json()["successful"][1]["task_name"] == "Bulk 2"
        assert len(response.json()["failed"]) == 0

    async def test_admin_can_delete_other_users_task(
        self,
        client: AsyncClient,
        test_user: dict,
        test_admin_login,
        fastapi_app: FastAPI,
        user_token,
        admin_token,
        test_admin,
        patch_challenge_and_conference_open,
    ):
        task_data = {
            "task_name": "Protect me",
            "task_abstract": "User only delete",
        }

        create_url = fastapi_app.url_path_for("create_task_route")
        create_resp = await client.post(
            f"{create_url}?challenge_id={CHALLENGE_ID}",
            json=task_data,
            headers={"Authorization": f"Bearer {user_token}"},
        )
        task_id = create_resp.json()["id"]

        delete_url = fastapi_app.url_path_for("delete_task_route_admin", id=task_id)
        response = await client.request(
            "DELETE",
            delete_url,
            params={"active_user_password": test_admin.password},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == status.HTTP_200_OK

    async def test_admin_can_bulk_delete_tasks(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        user_token,
        admin_token,
        test_admin,
        patch_challenge_and_conference_open,
    ):
        data = {
            "task_name": "Bulk 1",
            "task_abstract": "Abstract",
        }
        create_url = fastapi_app.url_path_for("create_task_route")
        resp1 = await client.post(
            f"{create_url}?challenge_id={CHALLENGE_ID}", json=data, headers={"Authorization": f"Bearer {user_token}"}
        )

        data["task_name"] = "Bulk 2"
        resp2 = await client.post(
            f"{create_url}?challenge_id={CHALLENGE_ID}", json=data, headers={"Authorization": f"Bearer {user_token}"}
        )
        ids = [resp1.json()["id"], resp2.json()["id"]]

        bulk_delete_url = fastapi_app.url_path_for("bulk_delete_tasks_route_admin")

        response = await client.request(
            "DELETE",
            bulk_delete_url,
            params={"active_user_password": test_admin.password},
            json=ids,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "Bulk delete completed" in response.json()["detail"]
        assert len(response.json()["successful"]) == 2
        assert len(response.json()["failed"]) == 0
