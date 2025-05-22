# backend/BMC_API/tests/test_admin_challenge_route.py
from unittest.mock import ANY, AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI, status
from fastapi.responses import FileResponse, StreamingResponse
from httpx import AsyncClient

from BMC_API.src.application.dependencies import get_challenge_service_admin
from BMC_API.src.application.use_cases.challenge_use_cases import ChallengeService
from BMC_API.src.application.use_cases.conference_use_cases import ConferenceService

pytest_plugins = [
    "BMC_API.tests.fixtures.admin_user_fixtures",
    "BMC_API.tests.fixtures.user_fixtures",
]

CONFERENCE_ID = 1


@pytest.fixture
def patch_challenge_and_conference():
    # Mocks
    mock_conference = MagicMock()
    mock_challenge = MagicMock(challenge_conference=mock_conference, challenge_status="Draft")

    with (
        patch.object(ConferenceService, "get_raw", new=AsyncMock(return_value=mock_conference)),
        patch.object(ChallengeService, "get_raw", new=AsyncMock(return_value=mock_challenge)),
    ):
        yield


@pytest.mark.anyio
class TestAdminChallengeRoutes:
    async def test_admin_can_create_challenge_with_extra_control(
        self, client: AsyncClient, fastapi_app: FastAPI, admin_token
    ):
        challenge_data = {
            "challenge_name": "Test Challenge",
            "challenge_abstract": "This is a challenge for testing.",
            "challenge_locked": False,
            "challenge_owner_id": 3,
        }

        url = fastapi_app.url_path_for("create_challenge_route_admin")

        response = await client.post(
            f"{url}?conference_id={CONFERENCE_ID}",
            json=challenge_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["challenge_name"] == challenge_data["challenge_name"]

    async def test_admin_can_access_other_users_challenge(
        self,
        client: AsyncClient,
        test_user: dict,
        test_admin_login,
        fastapi_app: FastAPI,
        user_token,
        admin_token,
    ):
        challenge_data = {
            "challenge_name": "UserTask",
            "challenge_abstract": "Owned by user",
        }

        create_url = fastapi_app.url_path_for("create_challenge_route")

        # Mock challenge only for creation process
        mock_conference = MagicMock(is_open_for_submissions=True)
        mock_challenge = MagicMock(challenge_conference=mock_conference)
        mock_task = MagicMock(task_challenge=mock_challenge)

        with (
            patch.object(ConferenceService, "get_raw", new=AsyncMock(return_value=mock_task)),
            patch.object(ChallengeService, "get_raw", new=AsyncMock(return_value=mock_challenge)),
        ):
            create_resp = await client.post(
                f"{create_url}?conference_id={CONFERENCE_ID}",
                json=challenge_data,
                headers={"Authorization": f"Bearer {user_token}"},
            )

            task_id = create_resp.json()["id"]

        # Continue without any mocking
        # Admin tries to get the challenge
        get_url = fastapi_app.url_path_for("get_challenge_route_admin", id=task_id)
        response = await client.get(get_url, headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["challenge_name"] == challenge_data["challenge_name"]
        assert response.json()["challenge_abstract"] == challenge_data["challenge_abstract"]

    async def test_admin_can_get_all_challenges(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, admin_token, patch_challenge_and_conference
    ):
        # First create challenges
        data = {
            "challenge_name": "Bulk 1",
            "challenge_abstract": "Abstract",
        }
        create_url = fastapi_app.url_path_for("create_challenge_route")
        response = await client.post(
            f"{create_url}?conference_id={CONFERENCE_ID}", json=data, headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_201_CREATED

        data["challenge_name"] = "Bulk 2"
        response = await client.post(
            f"{create_url}?conference_id={CONFERENCE_ID}", json=data, headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_201_CREATED

        get_url = fastapi_app.url_path_for("list_challenges_route_admin")
        response = await client.post(get_url, headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["total_pages"] == 1
        assert response.json()["total_records"] == 2
        assert len(response.json()["content"]) == 2
        assert response.json()["content"][0]["challenge_name"] == "Bulk 1"
        assert response.json()["content"][1]["challenge_name"] == "Bulk 2"

    async def test_admin_can_update_other_users_challenge(
        self,
        client: AsyncClient,
        test_user: dict,
        test_admin_login,
        fastapi_app: FastAPI,
        user_token,
        admin_token,
        patch_challenge_and_conference,
    ):
        challenge_data = {
            "challenge_name": "User Owned",
            "challenge_abstract": "Should be protected",
        }

        create_url = fastapi_app.url_path_for("create_challenge_route")
        create_resp = await client.post(
            f"{create_url}?conference_id={CONFERENCE_ID}",
            json=challenge_data,
            headers={"Authorization": f"Bearer {user_token}"},
        )
        task_id = create_resp.json()["id"]

        update_data = {
            "challenge_name": "Admin Attempt",
            "challenge_abstract": "Forbidden Update",
        }

        update_url = fastapi_app.url_path_for("update_challenge_route_admin", id=task_id)
        response = await client.put(update_url, json=update_data, headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["challenge_name"] == update_data["challenge_name"]
        assert response.json()["challenge_abstract"] == update_data["challenge_abstract"]

    async def test_admin_can_bulk_update_other_users_challenge(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, admin_token, patch_challenge_and_conference
    ):
        data = {
            "challenge_name": "Bulk 1",
            "challenge_abstract": "Abstract",
        }
        create_url = fastapi_app.url_path_for("create_challenge_route")
        resp1 = await client.post(
            f"{create_url}?conference_id={CONFERENCE_ID}", json=data, headers={"Authorization": f"Bearer {user_token}"}
        )
        conf_id1 = resp1.json()["id"]

        data["challenge_name"] = "Bulk 2"
        resp2 = await client.post(
            f"{create_url}?conference_id={CONFERENCE_ID}", json=data, headers={"Authorization": f"Bearer {user_token}"}
        )
        conf_id2 = resp2.json()["id"]

        bulk_update_url = fastapi_app.url_path_for("bulk_update_challenges_route_admin")
        updates = [
            {"id": conf_id1, "venue": "On-site"},
            {"id": conf_id2, "venue": "Remote"},
        ]

        response = await client.put(bulk_update_url, json=updates, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == status.HTTP_200_OK
        assert "Bulk update completed" in response.json()["detail"]
        assert len(response.json()["successful"]) == 2
        assert response.json()["successful"][0]["challenge_name"] == "Bulk 1"
        assert response.json()["successful"][1]["challenge_name"] == "Bulk 2"
        assert len(response.json()["failed"]) == 0

    async def test_admin_can_delete_other_users_challenge(
        self,
        client: AsyncClient,
        test_user: dict,
        test_admin_login,
        fastapi_app: FastAPI,
        user_token,
        admin_token,
        test_admin,
        patch_challenge_and_conference,
    ):
        challenge_data = {
            "challenge_name": "Protect me",
            "challenge_abstract": "User only delete",
        }

        create_url = fastapi_app.url_path_for("create_challenge_route")
        create_resp = await client.post(
            f"{create_url}?conference_id={CONFERENCE_ID}",
            json=challenge_data,
            headers={"Authorization": f"Bearer {user_token}"},
        )
        task_id = create_resp.json()["id"]

        delete_url = fastapi_app.url_path_for("delete_challenge_route_admin", id=task_id)
        response = await client.request(
            "DELETE",
            delete_url,
            params={"active_user_password": test_admin.password},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == status.HTTP_200_OK

    async def test_admin_can_bulk_delete_challenges(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        user_token,
        admin_token,
        test_admin,
        patch_challenge_and_conference,
    ):
        data = {
            "challenge_name": "Bulk 1",
            "challenge_abstract": "Abstract",
        }
        create_url = fastapi_app.url_path_for("create_challenge_route")
        resp1 = await client.post(
            f"{create_url}?conference_id={CONFERENCE_ID}", json=data, headers={"Authorization": f"Bearer {user_token}"}
        )

        data["challenge_name"] = "Bulk 2"
        resp2 = await client.post(
            f"{create_url}?conference_id={CONFERENCE_ID}", json=data, headers={"Authorization": f"Bearer {user_token}"}
        )
        ids = [resp1.json()["id"], resp2.json()["id"]]

        bulk_delete_url = fastapi_app.url_path_for("bulk_delete_challenges_route_admin")

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

    async def test_submit_challenge_route_admin(self, client: AsyncClient, fastapi_app: FastAPI, admin_token):
        challenge_id = 1
        with patch.object(ChallengeService, "submit_challenge", new=AsyncMock()) as mock_submit:
            url = fastapi_app.url_path_for("submit_challenge_route_admin", id=challenge_id)
            response = await client.put(url, headers={"Authorization": f"Bearer {admin_token}"})
            assert response.status_code == status.HTTP_200_OK
            assert response.json() == {
                "message": "Challenge successfully submitted. Challenge document is ready to download."
            }
            mock_submit.assert_awaited_once_with(
                id=challenge_id,
                background_tasks=ANY,
                send_notification_emails=False,
            )

    async def test_submit_challenge_route_admin_with_notification(
        self, client: AsyncClient, fastapi_app: FastAPI, admin_token
    ):
        challenge_id = 2
        with patch.object(ChallengeService, "submit_challenge", new=AsyncMock()) as mock_submit:
            url = fastapi_app.url_path_for("submit_challenge_route_admin", id=challenge_id)
            response = await client.put(
                f"{url}?send_notification_emails=true",
                headers={"Authorization": f"Bearer {admin_token}"},
            )
            assert response.status_code == status.HTTP_200_OK
            mock_submit.assert_awaited_once_with(
                id=challenge_id,
                background_tasks=ANY,
                send_notification_emails=True,
            )

    async def test_submit_challenge_route_admin_full_flow(
        self, client: AsyncClient, fastapi_app: FastAPI, admin_token, test_admin, dbsession
    ):
        # 1. Admin creates a new challenge
        challenge_payload = {"challenge_name": "Submit Challenge", "challenge_abstract": "End-to-end submit test"}
        create_ch_url = fastapi_app.url_path_for("create_challenge_route_admin")
        create_resp = await client.post(
            f"{create_ch_url}?conference_id={CONFERENCE_ID}",
            json=challenge_payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert create_resp.status_code == status.HTTP_201_CREATED
        challenge_id = create_resp.json()["id"]

        # 2. Add two tasks under that challenge (uses organizer role)
        task1_payload = {"task_name": "Task 1", "task_abstract": "First task"}
        create_task_url = fastapi_app.url_path_for("create_task_route_admin")
        task1 = await client.post(
            f"{create_task_url}?challenge_id={challenge_id}",
            json=task1_payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert task1.status_code == status.HTTP_201_CREATED

        task2_payload = {"task_name": "Task 2", "task_abstract": "Second task"}
        task2 = await client.post(
            f"{create_task_url}?challenge_id={challenge_id}",
            json=task2_payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert task2.status_code == status.HTTP_201_CREATED

        # IMPORTANT: force SQLAlchemy to flush and  reload relationships from the DB
        await dbsession.flush()
        dbsession.expire_all()

        # 3. Admin submits the challenge (this creates challenge + task histories)
        submit_url = fastapi_app.url_path_for("submit_challenge_route_admin", id=challenge_id)
        submit_resp = await client.put(
            submit_url,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert submit_resp.status_code == status.HTTP_200_OK

        # 3.1 Admin downloads the challenge
        download_url = fastapi_app.url_path_for("download_challenge_document_route_admin", id=challenge_id)
        download_resp = await client.get(
            download_url,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert download_resp.status_code == status.HTTP_200_OK
        assert download_resp.headers["content-type"] == "application/pdf"
        assert download_resp.content.startswith(b"%PDF-1.4")

        # 4. Check the challenge histories
        ch_hist_url = fastapi_app.url_path_for("get_challenge_history_admin", id=challenge_id)
        ch_hist_resp = await client.request(
            "get",
            ch_hist_url,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert ch_hist_resp.status_code == status.HTTP_200_OK
        result = ch_hist_resp.json()

        assert len(result["content"]) == 1
        assert result["content"][0]["id"] == challenge_id
        assert result["content"][0]["old_status"] == "Draft"
        assert result["content"][0]["new_status"] == "DraftSubmitted"
        assert result["content"][0]["snapshot"]["challenge_name"] == challenge_payload["challenge_name"]
        assert result["content"][0]["snapshot"]["challenge_abstract"] == challenge_payload["challenge_abstract"]

        # 5. Check the task histories
        ## Task 1
        tsk_hist_url = fastapi_app.url_path_for("get_task_history_admin", id=task1.json()["id"])
        tsk_hist_resp = await client.request(
            "get",
            tsk_hist_url,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert tsk_hist_resp.status_code == status.HTTP_200_OK
        result = tsk_hist_resp.json()

        assert len(result["content"]) == 1
        assert result["content"][0]["id"] == task1.json()["id"]
        assert result["content"][0]["old_status"] == "Draft"
        assert result["content"][0]["new_status"] == "DraftSubmitted"
        assert result["content"][0]["snapshot"]["task_name"] == task1_payload["task_name"]
        assert result["content"][0]["snapshot"]["task_abstract"] == task1_payload["task_abstract"]

        ## Task 2
        tsk_hist_url = fastapi_app.url_path_for("get_task_history_admin", id=task2.json()["id"])
        tsk_hist_resp = await client.request(
            "get",
            tsk_hist_url,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert tsk_hist_resp.status_code == status.HTTP_200_OK
        result = tsk_hist_resp.json()

        assert len(result["content"]) == 1
        assert result["content"][0]["id"] == task2.json()["id"]
        assert result["content"][0]["old_status"] == "Draft"
        assert result["content"][0]["new_status"] == "DraftSubmitted"
        assert result["content"][0]["snapshot"]["task_name"] == task2_payload["task_name"]
        assert result["content"][0]["snapshot"]["task_abstract"] == task2_payload["task_abstract"]

    async def test_update_challenge_status_route_admin(self, client: AsyncClient, fastapi_app: FastAPI, admin_token):
        challenge_id = 3
        dummy = {
            "id": challenge_id,
            "challenge_status": "Accept",
            "challenge_name": "Foo",
            "challenge_abstract": "Bar",
        }
        with patch.object(ChallengeService, "status", new=AsyncMock(return_value=dummy)):
            url = fastapi_app.url_path_for("update_challenge_status_route_admin", id=challenge_id)
            response = await client.put(
                url,
                json={"challenge_status": "Accept"},
                headers={"Authorization": f"Bearer {admin_token}"},
            )

            assert response.status_code == status.HTTP_200_OK
            assert response.json()["challenge_status"] == "Accept"

    async def test_bulk_update_challenge_status_route_admin(
        self, client: AsyncClient, fastapi_app: FastAPI, admin_token
    ):
        ids = [1, 2]
        result = {
            "detail": "Bulk status update completed",
            "successful": [{"id": 1, "challenge_name": "Test challenge", "challenge_status": "Reject"}],
            "failed": [],
        }
        with patch.object(ChallengeService, "bulk_status", new=AsyncMock(return_value=result)):
            url = fastapi_app.url_path_for("bulk_update_challenge_status_route_admin")
            response = await client.put(
                url,
                json={"ids": ids, "challenge_status_object": {"challenge_status": "Reject"}},
                headers={"Authorization": f"Bearer {admin_token}"},
            )

            assert response.status_code == status.HTTP_200_OK
            assert response.json()["detail"] == "Bulk status update completed"
            assert len(response.json()["successful"]) == 1

    async def test_download_challenge_document_route_admin(
        self, client: AsyncClient, fastapi_app: FastAPI, admin_token, tmp_path
    ):
        challenge_id = 4
        dummy_pdf = tmp_path / "dummy.pdf"
        dummy_pdf.write_bytes(b"%PDF-1.0")
        with patch.object(
            ChallengeService,
            "download_challenge",
            new=AsyncMock(return_value=FileResponse(str(dummy_pdf))),
        ):
            url = fastapi_app.url_path_for("download_challenge_document_route_admin", id=challenge_id)
            response = await client.get(url, headers={"Authorization": f"Bearer {admin_token}"})
            assert response.status_code == status.HTTP_200_OK
            assert response.headers["content-type"] == "application/pdf"

    async def test_bulk_download_challenge_document_route_admin(
        self, client: AsyncClient, fastapi_app: FastAPI, admin_token
    ):
        ids = [5, 6]
        stream = StreamingResponse(iter([b"a", b"b"]), media_type="application/octet-stream")
        with patch.object(
            ChallengeService,
            "download_challenge_bulk",
            new=AsyncMock(return_value=stream),
        ):
            url = fastapi_app.url_path_for("bulk_download_challenge_document_route_admin")
            response = await client.post(url, json=ids, headers={"Authorization": f"Bearer {admin_token}"})
            assert response.status_code == status.HTTP_200_OK

    async def test_take_snapshot_route_admin(self, client: AsyncClient, fastapi_app: FastAPI, admin_token):
        challenge_id = 7
        with patch.object(ChallengeService, "take_snapshot", new=AsyncMock()) as mock_snap:
            url = fastapi_app.url_path_for("take_snapshot_route_admin", id=challenge_id)
            response = await client.get(url, headers={"Authorization": f"Bearer {admin_token}"})
            assert response.status_code == status.HTTP_200_OK
            assert response.json() == {"message": "Snapshot created successfully."}
            mock_snap.assert_awaited_once_with(id=challenge_id)

    async def test_get_challenge_history_admin(self, client: AsyncClient, fastapi_app: FastAPI, admin_token):
        challenge_id = 8
        histories = [{"status": "Draft", "timestamp": "2025-05-08T10:00:00"}]
        with patch.object(
            ChallengeService,
            "challenge_histories",
            new=AsyncMock(return_value=(histories, 1, 1)),
        ):
            url = fastapi_app.url_path_for("get_challenge_history_admin", id=challenge_id)
            response = await client.get(url, headers={"Authorization": f"Bearer {admin_token}"})
            assert response.status_code == status.HTTP_200_OK
            body = response.json()
            assert body["total_pages"] == 1
            assert body["total_records"] == 1
            assert body["content"] == histories

    @pytest.mark.anyio
    async def test_delete_challenge_history_route_admin(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        admin_token: str,
        test_admin,
    ):
        history_id = 9

        # 1) Build a fake service instance with a mock delete()
        fake_svc = MagicMock()
        fake_svc.challenge_history_service = MagicMock()
        fake_svc.challenge_history_service.delete = AsyncMock()

        # 2) Override the DI for this one test
        fastapi_app.dependency_overrides[get_challenge_service_admin] = lambda: fake_svc

        # 3) Exercise the route
        url = fastapi_app.url_path_for("delete_challenge_history_route_admin", id=history_id)
        response = await client.delete(
            url,
            params={"active_user_password": test_admin.password},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        # 4) Always clear overrides so other tests aren’t affected
        fastapi_app.dependency_overrides.clear()

        # 5) Assert you get your 200 and that your mock was called
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"detail": "Challenge history deleted"}
        fake_svc.challenge_history_service.delete.assert_awaited_once_with(id=history_id)

    async def test_prune_challenge_route_admin(
        self, client: AsyncClient, fastapi_app: FastAPI, admin_token, test_admin
    ):
        challenge_id = 10
        result = {"detail": "Pruned", "successful": [{"id": 10}], "failed": []}
        with patch.object(
            ChallengeService,
            "prune_challenge",
            new=AsyncMock(return_value=result),
        ):
            url = fastapi_app.url_path_for("prune_challenge_route_admin", id=challenge_id)
            response = await client.request(
                "DELETE",
                url,
                params={"active_user_password": test_admin.password},
                headers={"Authorization": f"Bearer {admin_token}"},
            )
            assert response.status_code == status.HTTP_200_OK
            assert response.json() == result

    async def test_prune_challenge_route_admin_full_flow(
        self, client: AsyncClient, fastapi_app: FastAPI, admin_token, test_admin, dbsession
    ):
        # 1. Admin creates a new challenge
        challenge_payload = {"challenge_name": "Prune Challenge", "challenge_abstract": "End-to-end prune test"}
        create_ch_url = fastapi_app.url_path_for("create_challenge_route_admin")
        create_resp = await client.post(
            f"{create_ch_url}?conference_id={CONFERENCE_ID}",
            json=challenge_payload,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert create_resp.status_code == status.HTTP_201_CREATED
        challenge_id = create_resp.json()["id"]

        # 2. Add two tasks under that challenge (uses organizer role)
        create_task_url = fastapi_app.url_path_for("create_task_route_admin")
        task1 = await client.post(
            f"{create_task_url}?challenge_id={challenge_id}",
            json={"task_name": "Task 1", "task_abstract": "First task"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert task1.status_code == status.HTTP_201_CREATED

        task2 = await client.post(
            f"{create_task_url}?challenge_id={challenge_id}",
            json={"task_name": "Task 2", "task_abstract": "Second task"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert task2.status_code == status.HTTP_201_CREATED

        # IMPORTANT: force SQLAlchemy to flush and  reload relationships from the DB
        await dbsession.flush()
        dbsession.expire_all()

        # 3. Admin submits the challenge (this creates challenge + task histories)
        submit_url = fastapi_app.url_path_for("submit_challenge_route_admin", id=challenge_id)
        submit_resp = await client.put(
            submit_url,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert submit_resp.status_code == status.HTTP_200_OK

        # 3.1 Admin downloads the challenge
        download_url = fastapi_app.url_path_for("download_challenge_document_route_admin", id=challenge_id)
        download_resp = await client.get(
            download_url,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert download_resp.status_code == status.HTTP_200_OK
        assert download_resp.headers["content-type"] == "application/pdf"
        assert download_resp.content.startswith(b"%PDF-1.4")

        # 4. Prune the challenge (deletes challenge, its histories, tasks & their histories)
        prune_url = fastapi_app.url_path_for("prune_challenge_route_admin", id=challenge_id)
        prune_resp = await client.request(
            "DELETE",
            prune_url,
            params={"active_user_password": test_admin.password},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert prune_resp.status_code == status.HTTP_200_OK
        result = prune_resp.json()

        # should have removed the challenge itself
        assert len(result["successful"]["challenge"]) == 1
        assert challenge_id in result["successful"]["challenge"]
        assert len(result["successful"]["challenge histories"]) == 1

        assert len(result["successful"]["tasks"]) == 2
        assert task1.json()["id"] in result["successful"]["tasks"]
        assert task2.json()["id"] in result["successful"]["tasks"]
        assert len(result["successful"]["task histories"]) == 2

        # Verify the challenge is truly gone
        get_admin_url = fastapi_app.url_path_for("get_challenge_route_admin", id=challenge_id)
        missing = await client.get(get_admin_url, headers={"Authorization": f"Bearer {admin_token}"})
        assert missing.status_code == status.HTTP_404_NOT_FOUND
