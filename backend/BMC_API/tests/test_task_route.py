# backend/BMC_API/tests/test_task_route.py
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from BMC_API.src.application.use_cases.challenge_use_cases import ChallengeService
from BMC_API.src.application.use_cases.task_use_cases import TaskService

pytest_plugins = [
    "BMC_API.tests.fixtures.user_fixtures",
]

CHALLENGE_ID = 1


@pytest.fixture
def patch_challenge_and_conference_open():
    # Mocks
    mock_conference = MagicMock(is_open_for_submissions=True)
    mock_challenge = MagicMock(challenge_conference=mock_conference, challenge_status="Draft")
    mock_task = MagicMock(task_challenge=mock_challenge, task_status="Draft")

    with (
        patch.object(TaskService, "get_raw", new=AsyncMock(return_value=mock_task)),
        patch.object(ChallengeService, "get_raw", new=AsyncMock(return_value=mock_challenge)),
    ):
        yield


@pytest.mark.anyio
class TestTaskRoutes:
    async def test_create_task_authenticated(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, patch_challenge_and_conference_open
    ):
        #

        task_data = {"task_name": "Test Task", "task_abstract": "This is a task for testing."}

        url = fastapi_app.url_path_for("create_task_route")
        response = await client.post(
            f"{url}?challenge_id={CHALLENGE_ID}", json=task_data, headers={"Authorization": f"Bearer {user_token}"}
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["task_name"] == task_data["task_name"]

    async def test_create_task_authenticated_with_extra_fields(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, patch_challenge_and_conference_open
    ):
        task_data = {"task_name": "Test Task", "extra_field": "This is a task for testing."}

        url = fastapi_app.url_path_for("create_task_route")
        response = await client.post(
            f"{url}?challenge_id={CHALLENGE_ID}", json=task_data, headers={"Authorization": f"Bearer {user_token}"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["msg"] == "Extra inputs are not permitted"

    async def test_create_task_unauthenticated(self, client: AsyncClient, fastapi_app: FastAPI):
        # Act: No token provided
        url = fastapi_app.url_path_for("create_task_route")
        response = await client.post(
            f"{url}?challenge_id={CHALLENGE_ID}",
            json={
                "task_name": "Unauth Task",
                "task_abstract": "No auth token",
            },
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_create_task_missing_fields(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, patch_challenge_and_conference_open
    ):
        incomplete_data = {"task_name": "Missing Description", "task_deadline": str(datetime.now())}

        url = fastapi_app.url_path_for("create_task_route")
        response = await client.post(
            f"{url}?challenge_id={CHALLENGE_ID}",
            json=incomplete_data,
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_create_and_access_task_as_different_user(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        user_token,
        login_user_factory,
        test_user2,
        patch_challenge_and_conference_open,
    ):
        # Step 1: test_user creates a task
        task_data = {
            "task_name": "User's Task",
            "task_abstract": "Should not be accessible by others.",
        }
        url = fastapi_app.url_path_for("create_task_route")
        create_response = await client.post(
            f"{url}?challenge_id={CHALLENGE_ID}", json=task_data, headers={"Authorization": f"Bearer {user_token}"}
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        task_id = create_response.json()["id"]

        # Step 2: test_user2 tries to fetch it (should fail)
        user2_token = await login_user_factory(test_user2)
        get_url = fastapi_app.url_path_for("get_task_route", id=task_id)
        response = await client.get(get_url, headers={"Authorization": f"Bearer {user2_token}"})

        # Admin does NOT own the task, should be forbidden
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_create_task_with_locked_challenge(self, client: AsyncClient, fastapi_app: FastAPI, user_token):
        task_data = {
            "task_name": "Initial",
            "task_abstract": "Start",
        }

        url = fastapi_app.url_path_for("create_task_route")

        # Mocks
        mock_conference = MagicMock(is_open_for_submissions=False)
        mock_challenge = MagicMock(challenge_conference=mock_conference)
        mock_task = MagicMock(task_challenge=mock_challenge)

        with (
            patch.object(TaskService, "get_raw", new=AsyncMock(return_value=mock_task)),
            patch.object(ChallengeService, "get_raw", new=AsyncMock(return_value=mock_challenge)),
        ):
            response = await client.post(
                f"{url}?challenge_id={CHALLENGE_ID}", json=task_data, headers={"Authorization": f"Bearer {user_token}"}
            )

        assert response.status_code == status.HTTP_423_LOCKED

    async def test_get_task_by_id(self, client: AsyncClient, fastapi_app: FastAPI, user_token):
        task_data = {
            "task_name": "Get Task",
            "task_abstract": "To retrieve.",
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
        get_url = fastapi_app.url_path_for("get_task_route", id=task_id)
        response = await client.get(get_url, headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == task_id

    async def test_get_all_my_tasks(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, patch_challenge_and_conference_open
    ):
        task_data = {
            "task_name": "Get Task",
            "task_abstract": "To retrieve.",
        }

        url = fastapi_app.url_path_for("create_task_route")
        await client.post(
            f"{url}?challenge_id={CHALLENGE_ID}", json=task_data, headers={"Authorization": f"Bearer {user_token}"}
        )

        get_url = fastapi_app.url_path_for("my_tasks_route")
        response = await client.get(get_url, headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["total_pages"] == 1
        assert response.json()["total_records"] == 1
        assert len(response.json()["content"]) == 1
        assert response.json()["content"][0]["task_name"] == task_data["task_name"]

    async def test_update_task(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, patch_challenge_and_conference_open
    ):
        task_data = {
            "task_name": "Initial",
            "task_abstract": "Start",
        }

        url = fastapi_app.url_path_for("create_task_route")
        create_resp = await client.post(
            f"{url}?challenge_id={CHALLENGE_ID}", json=task_data, headers={"Authorization": f"Bearer {user_token}"}
        )
        task_id = create_resp.json()["id"]

        update_data = {
            "task_name": "Updated",
            "task_abstract": "Changed desc",
        }

        update_url = fastapi_app.url_path_for("update_task_route", id=task_id)
        response = await client.put(update_url, json=update_data, headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["task_name"] == update_data["task_name"]

    async def test_update_task_unauthorized_user(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        login_user_factory,
        user_token,
        test_user2,
        patch_challenge_and_conference_open,
    ):
        # Step 1: test_user creates a task
        task_data = {
            "task_name": "UserTask",
            "task_abstract": "User-owned",
        }
        url = fastapi_app.url_path_for("create_task_route")
        create_response = await client.post(
            f"{url}?challenge_id={CHALLENGE_ID}", json=task_data, headers={"Authorization": f"Bearer {user_token}"}
        )
        task_id = create_response.json()["id"]

        # Step 2: test_user2 tries to update it (should fail)
        user2_token = await login_user_factory(test_user2)
        update_data = {
            "task_name": "Admin Attempt",
            "task_abstract": "Should not be allowed",
        }

        update_url = fastapi_app.url_path_for("update_task_route", id=task_id)
        response = await client.put(update_url, json=update_data, headers={"Authorization": f"Bearer {user2_token}"})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_update_invalid_task_id(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, patch_challenge_and_conference_open
    ):
        update_data = {
            "task_name": "Invalid update",
            "task_abstract": "Invalid ID",
        }

        invalid_id = 999999
        url = fastapi_app.url_path_for("update_task_route", id=invalid_id)
        response = await client.put(url, json=update_data, headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code in {status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN}

    async def test_delete_task(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, patch_challenge_and_conference_open
    ):
        task_data = {
            "task_name": "To Delete",
            "task_abstract": "Delete me",
        }

        url = fastapi_app.url_path_for("create_task_route")
        create_resp = await client.post(
            f"{url}?challenge_id={CHALLENGE_ID}", json=task_data, headers={"Authorization": f"Bearer {user_token}"}
        )
        task_id = create_resp.json()["id"]

        delete_url = fastapi_app.url_path_for("delete_task_route", id=task_id)
        response = await client.delete(delete_url, headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["detail"] == "Task deleted"

    async def test_delete_task_unauthorized_user(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        login_user_factory,
        user_token,
        test_user2,
        patch_challenge_and_conference_open,
    ):
        # Step 1: test_user creates a task
        task_data = {
            "task_name": "To be protected",
            "task_abstract": "Delete attempt blocked",
        }

        create_url = fastapi_app.url_path_for("create_task_route")
        create_response = await client.post(
            f"{create_url}?challenge_id={CHALLENGE_ID}",
            json=task_data,
            headers={"Authorization": f"Bearer {user_token}"},
        )
        task_id = create_response.json()["id"]

        # Step 2: test_user2 tries to delete it (should fail)
        user2_token = await login_user_factory(test_user2)
        delete_url = fastapi_app.url_path_for("delete_task_route", id=task_id)
        response = await client.delete(delete_url, headers={"Authorization": f"Bearer {user2_token}"})

        assert response.status_code == status.HTTP_403_FORBIDDEN
