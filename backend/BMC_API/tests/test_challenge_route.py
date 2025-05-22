# backend/BMC_API/tests/test_challenge_route.py
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI, status
from fastapi.responses import FileResponse
from httpx import AsyncClient

from BMC_API.src.application.use_cases.challenge_use_cases import ChallengeService
from BMC_API.src.application.use_cases.conference_use_cases import ConferenceService
from BMC_API.src.application.use_cases.task_use_cases import TaskService

pytest_plugins = [
    "BMC_API.tests.fixtures.user_fixtures",
    "BMC_API.tests.fixtures.admin_user_fixtures",
]

CONFERENCE_ID = 1


@pytest.fixture
def patch_challenge_and_conference_open():
    # Mocks
    mock_conference = MagicMock(is_open_for_submissions=True)
    mock_challenge = MagicMock(challenge_conference=mock_conference, challenge_status="Draft")

    with (
        patch.object(ConferenceService, "get_raw", new=AsyncMock(return_value=mock_conference)),
        patch.object(ChallengeService, "get_raw", new=AsyncMock(return_value=mock_challenge)),
    ):
        yield


@pytest.mark.anyio
class TestChallengeRoutes:
    async def test_create_challenge_authenticated(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, patch_challenge_and_conference_open
    ):
        #

        challenge_data = {"challenge_name": "Test Challenge", "challenge_abstract": "This is a challenge for testing."}

        url = fastapi_app.url_path_for("create_challenge_route")
        response = await client.post(
            f"{url}?conference_id={CONFERENCE_ID}",
            json=challenge_data,
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["challenge_name"] == challenge_data["challenge_name"]

    async def test_create_challenge_authenticated_with_extra_fields(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, patch_challenge_and_conference_open
    ):
        challenge_data = {"challenge_name": "Test Challenge", "extra_field": "This is a challenge for testing."}

        url = fastapi_app.url_path_for("create_challenge_route")
        response = await client.post(
            f"{url}?conference_id={CONFERENCE_ID}",
            json=challenge_data,
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["msg"] == "Extra inputs are not permitted"

    async def test_create_challenge_unauthenticated(self, client: AsyncClient, fastapi_app: FastAPI):
        # Act: No token provided
        url = fastapi_app.url_path_for("create_challenge_route")
        response = await client.post(
            f"{url}?conference_id={CONFERENCE_ID}",
            json={
                "challenge_name": "Unauth Challenge",
                "challenge_abstract": "No auth token",
            },
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_create_challenge_extra_fields(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, patch_challenge_and_conference_open
    ):
        incomplete_data = {"challenge_name": "Missing Description", "challenge_deadline": str(datetime.now())}

        url = fastapi_app.url_path_for("create_challenge_route")
        response = await client.post(
            f"{url}?conference_id={CONFERENCE_ID}",
            json=incomplete_data,
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_create_and_access_challenge_as_different_user(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        user_token,
        login_user_factory,
        test_user2,
        patch_challenge_and_conference_open,
    ):
        # Step 1: test_user creates a challenge
        challenge_data = {
            "challenge_name": "User's Challenge",
            "challenge_abstract": "Should not be accessible by others.",
        }
        url = fastapi_app.url_path_for("create_challenge_route")
        create_response = await client.post(
            f"{url}?conference_id={CONFERENCE_ID}",
            json=challenge_data,
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        challenge_id = create_response.json()["id"]

        # Step 2: test_user2 tries to fetch it (should fail)
        user2_token = await login_user_factory(test_user2)
        get_url = fastapi_app.url_path_for("get_challenge_route", id=challenge_id)
        response = await client.get(get_url, headers={"Authorization": f"Bearer {user2_token}"})

        # Admin does NOT own the challenge, should be forbidden
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_create_challenge_with_locked_challenge(self, client: AsyncClient, fastapi_app: FastAPI, user_token):
        challenge_data = {
            "challenge_name": "Initial",
            "challenge_abstract": "Start",
        }

        url = fastapi_app.url_path_for("create_challenge_route")

        # Mock challenge only for creation process
        mock_conference = MagicMock(is_open_for_submissions=False)

        with patch.object(ConferenceService, "get_raw", new=AsyncMock(return_value=mock_conference)):
            response = await client.post(
                f"{url}?conference_id={CONFERENCE_ID}",
                json=challenge_data,
                headers={"Authorization": f"Bearer {user_token}"},
            )

        assert response.status_code == status.HTTP_423_LOCKED

    async def test_get_challenge_by_id(self, client: AsyncClient, fastapi_app: FastAPI, user_token):
        challenge_data = {
            "challenge_name": "Get Challenge",
            "challenge_abstract": "To retrieve.",
        }

        create_url = fastapi_app.url_path_for("create_challenge_route")

        # Mock challenge only for creation process
        mock_conference = MagicMock(is_open_for_submissions=True)
        mock_challenge = MagicMock(challenge_conference=mock_conference)

        with (
            patch.object(ConferenceService, "get_raw", new=AsyncMock(return_value=mock_conference)),
            patch.object(ChallengeService, "get_raw", new=AsyncMock(return_value=mock_challenge)),
        ):
            create_resp = await client.post(
                f"{create_url}?conference_id={CONFERENCE_ID}",
                json=challenge_data,
                headers={"Authorization": f"Bearer {user_token}"},
            )

            challenge_id = create_resp.json()["id"]

        # Continue without any mocking
        get_url = fastapi_app.url_path_for("get_challenge_route", id=challenge_id)
        response = await client.get(get_url, headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == challenge_id

    async def test_get_all_my_challenges(self, client: AsyncClient, fastapi_app: FastAPI, user_token):
        challenge_data = {
            "challenge_name": "Get Challenge",
            "challenge_abstract": "To retrieve.",
        }

        url = fastapi_app.url_path_for("create_challenge_route")

        # Mock challenge only for creation process
        mock_conference = MagicMock(is_open_for_submissions=True)

        with (
            patch.object(ConferenceService, "get_raw", new=AsyncMock(return_value=mock_conference)),
        ):
            response = await client.post(
                f"{url}?conference_id={CONFERENCE_ID}",
                json=challenge_data,
                headers={"Authorization": f"Bearer {user_token}"},
            )

        get_url = fastapi_app.url_path_for("my_challenges_route")
        response = await client.get(get_url, headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["total_pages"] == 1
        assert response.json()["total_records"] == 1
        assert len(response.json()["content"]) == 1
        assert response.json()["content"][0]["challenge_name"] == challenge_data["challenge_name"]

    async def test_update_challenge(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, patch_challenge_and_conference_open
    ):
        challenge_data = {
            "challenge_name": "Initial",
            "challenge_abstract": "Start",
        }

        url = fastapi_app.url_path_for("create_challenge_route")
        create_resp = await client.post(
            f"{url}?conference_id={CONFERENCE_ID}",
            json=challenge_data,
            headers={"Authorization": f"Bearer {user_token}"},
        )
        challenge_id = create_resp.json()["id"]

        update_data = {
            "challenge_name": "Updated",
            "challenge_abstract": "Changed desc",
        }

        update_url = fastapi_app.url_path_for("update_challenge_route", id=challenge_id)
        response = await client.put(update_url, json=update_data, headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["challenge_name"] == update_data["challenge_name"]

    async def test_update_challenge_unauthorized_user(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        login_user_factory,
        user_token,
        test_user2,
        patch_challenge_and_conference_open,
    ):
        # Step 1: test_user creates a challenge
        challenge_data = {
            "challenge_name": "Userchallenge",
            "challenge_abstract": "User-owned",
        }
        url = fastapi_app.url_path_for("create_challenge_route")
        create_response = await client.post(
            f"{url}?conference_id={CONFERENCE_ID}",
            json=challenge_data,
            headers={"Authorization": f"Bearer {user_token}"},
        )
        challenge_id = create_response.json()["id"]

        # Step 2: test_user2 tries to update it (should fail)
        user2_token = await login_user_factory(test_user2)
        update_data = {
            "challenge_name": "Admin Attempt",
            "challenge_abstract": "Should not be allowed",
        }

        update_url = fastapi_app.url_path_for("update_challenge_route", id=challenge_id)
        response = await client.put(update_url, json=update_data, headers={"Authorization": f"Bearer {user2_token}"})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_update_invalid_conference_id(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, patch_challenge_and_conference_open
    ):
        update_data = {
            "challenge_name": "Invalid update",
            "challenge_abstract": "Invalid ID",
        }

        invalid_id = 999999
        url = fastapi_app.url_path_for("update_challenge_route", id=invalid_id)
        response = await client.put(url, json=update_data, headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code in {status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN}

    async def test_delete_challenge(
        self, client: AsyncClient, fastapi_app: FastAPI, user_token, test_user, patch_challenge_and_conference_open
    ):
        challenge_data = {
            "challenge_name": "To Delete",
            "challenge_abstract": "Delete me",
        }

        url = fastapi_app.url_path_for("create_challenge_route")
        create_resp = await client.post(
            f"{url}?conference_id={CONFERENCE_ID}",
            json=challenge_data,
            headers={"Authorization": f"Bearer {user_token}"},
        )
        challenge_id = create_resp.json()["id"]

        delete_url = fastapi_app.url_path_for("delete_challenge_route", id=challenge_id)
        response = await client.delete(delete_url, params={"active_user_password": test_user.password}, headers={"Authorization": f"Bearer {user_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["detail"] == "Challenge deleted"

    async def test_delete_challenge_unauthorized_user(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        login_user_factory,
        user_token,
        test_user2,
        patch_challenge_and_conference_open,
    ):
        # Step 1: test_user creates a challenge
        challenge_data = {
            "challenge_name": "To be protected",
            "challenge_abstract": "Delete attempt blocked",
        }

        create_url = fastapi_app.url_path_for("create_challenge_route")
        create_response = await client.post(
            f"{create_url}?conference_id={CONFERENCE_ID}",
            json=challenge_data,
            headers={"Authorization": f"Bearer {user_token}"},
        )
        challenge_id = create_response.json()["id"]

        # Step 2: test_user2 tries to delete it (should fail)
        user2_token = await login_user_factory(test_user2)
        delete_url = fastapi_app.url_path_for("delete_challenge_route", id=challenge_id)
        response = await client.delete(delete_url, headers={"Authorization": f"Bearer {user2_token}"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_submit_challenge_success(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        user_token,
        patch_challenge_and_conference_open,
    ):
        # Create a challenge first to get its ID
        create_url = fastapi_app.url_path_for("create_challenge_route")
        resp = await client.post(
            f"{create_url}?conference_id={CONFERENCE_ID}",
            json={
                "challenge_name": "Submit Me",
                "challenge_abstract": "Testing submit.",
            },
            headers={"Authorization": f"Bearer {user_token}"},
        )
        challenge_id = resp.json()["id"]

        # Patch out the actual send logic
        with patch.object(ChallengeService, "submit_challenge", new=AsyncMock()) as mock_submit:
            submit_url = fastapi_app.url_path_for("submit_challenge_route", id=challenge_id)
            response = await client.put(
                submit_url,
                headers={"Authorization": f"Bearer {user_token}"},
            )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == (
            "Challenge successfully submitted. Challenge document is ready to download."
        )
        mock_submit.assert_awaited_once()

    async def test_submit_challenge_locked(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        user_token,
        patch_challenge_and_conference_open,
    ):
        # Create a challenge first to get its ID
        create_url = fastapi_app.url_path_for("create_challenge_route")
        resp = await client.post(
            f"{create_url}?conference_id={CONFERENCE_ID}",
            json={
                "challenge_name": "Submit Me",
                "challenge_abstract": "Testing submit.",
            },
            headers={"Authorization": f"Bearer {user_token}"},
        )

        challenge_id = resp.json()["id"]

        # Simulate a challenge no longer editable and conference closed
        mock_ch = MagicMock(is_allowed_for_further_editing=False, challenge_conference_id=CONFERENCE_ID)
        mock_conf = MagicMock(is_open_for_submissions=False)

        with (
            patch.object(ChallengeService, "get_raw", new=AsyncMock(return_value=mock_ch)),
            patch.object(ConferenceService, "get_raw", new=AsyncMock(return_value=mock_conf)),
        ):
            submit_url = fastapi_app.url_path_for("submit_challenge_route", id=challenge_id)
            response = await client.put(
                submit_url,
                headers={"Authorization": f"Bearer {user_token}"},
            )

        assert response.status_code == status.HTTP_423_LOCKED

    async def test_submit_challenge_unauthorized_user(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        login_user_factory,
        user_token,
        test_user2,
        patch_challenge_and_conference_open,
    ):
        # Create under user1
        create_url = fastapi_app.url_path_for("create_challenge_route")
        create_resp = await client.post(
            f"{create_url}?conference_id={CONFERENCE_ID}",
            json={"challenge_name": "Private", "challenge_abstract": "No peeking."},
            headers={"Authorization": f"Bearer {user_token}"},
        )
        cid = create_resp.json()["id"]

        user2_token = await login_user_factory(test_user2)
        submit_url = fastapi_app.url_path_for("submit_challenge_route", id=cid)
        response = await client.put(
            submit_url,
            headers={"Authorization": f"Bearer {user2_token}"},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_download_challenge_document_success(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        user_token,
        patch_challenge_and_conference_open,
        tmp_path,
    ):
        # Create challenge in DB
        create_url = fastapi_app.url_path_for("create_challenge_route")
        create_resp = await client.post(
            f"{create_url}?conference_id={CONFERENCE_ID}",
            json={"challenge_name": "DL Test", "challenge_abstract": "Download me."},
            headers={"Authorization": f"Bearer {user_token}"},
        )
        cid = create_resp.json()["id"]

        # Create a dummy PDF file
        pdf_path = tmp_path / "foo.pdf"
        pdf_path.write_bytes(b"%PDF-1.4 fake content")

        # Patch the service to return our FileResponse
        fake_file = FileResponse(
            str(pdf_path),
            media_type="application/pdf",
            filename="foo.pdf",
        )
        with patch.object(ChallengeService, "download_challenge", new=AsyncMock(return_value=fake_file)):
            dl_url = fastapi_app.url_path_for("download_challenge_document_route", id=cid)
            response = await client.get(
                dl_url,
                headers={"Authorization": f"Bearer {user_token}"},
            )

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/pdf"
        assert response.content.startswith(b"%PDF-1.4")

    async def test_download_challenge_document_unauthorized_user(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        login_user_factory,
        user_token,
        test_user2,
        patch_challenge_and_conference_open,
        tmp_path,
    ):
        # Create challenge under user1
        create_url = fastapi_app.url_path_for("create_challenge_route")
        create_resp = await client.post(
            f"{create_url}?conference_id={CONFERENCE_ID}",
            json={"challenge_name": "Secret DL", "challenge_abstract": "No access."},
            headers={"Authorization": f"Bearer {user_token}"},
        )
        cid = create_resp.json()["id"]

        user2_token = await login_user_factory(test_user2)
        dl_url = fastapi_app.url_path_for("download_challenge_document_route", id=cid)
        response = await client.get(
            dl_url,
            headers={"Authorization": f"Bearer {user2_token}"},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_submit_challenge_route_full_flow(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        user_token,
        admin_token,
        dbsession,
    ):
        # Arrange mocks
        mock_conference = MagicMock(id=CONFERENCE_ID, is_open_for_submissions=True)
        mock_challenge = MagicMock(challenge_conference=mock_conference)
        mock_task = MagicMock(task_challenge=mock_challenge)
        orig_get_raw = TaskService.get_raw

        async def get_raw_once(self, *args, **kwargs):
            # on the very first call, hand back your mock…
            if not getattr(get_raw_once, "_already_called", False):
                setattr(get_raw_once, "_already_called", True)
                return mock_task
            # …after that, delegate to the real method
            setattr(get_raw_once, "_already_called", False)
            return await orig_get_raw(self, *args, **kwargs)

        # 1. User creates a new challenge
        with patch.object(ConferenceService, "get_raw", new=AsyncMock(return_value=mock_conference)):
            challenge_payload = {"challenge_name": "Submit Challenge", "challenge_abstract": "End-to-end submit test"}
            create_ch_url = fastapi_app.url_path_for("create_challenge_route")
            create_resp = await client.post(
                f"{create_ch_url}?conference_id={CONFERENCE_ID}",
                json=challenge_payload,
                headers={"Authorization": f"Bearer {user_token}"},
            )
        assert create_resp.status_code == status.HTTP_201_CREATED

        challenge_id = create_resp.json()["id"]

        # 2. User adds two tasks under that challenge (uses organizer role)

        with patch.object(ChallengeService, "get_raw", new=AsyncMock(return_value=mock_challenge)):
            task1_payload = {"task_name": "Task 1", "task_abstract": "First task"}
            create_task_url = fastapi_app.url_path_for("create_task_route")
            task1 = await client.post(
                f"{create_task_url}?challenge_id={challenge_id}",
                json=task1_payload,
                headers={"Authorization": f"Bearer {user_token}"},
            )

            assert task1.status_code == status.HTTP_201_CREATED
            task1_id = task1.json()["id"]

            task2_payload = {"task_name": "Task 2", "task_abstract": "Second task"}
            task2 = await client.post(
                f"{create_task_url}?challenge_id={challenge_id}",
                json=task2_payload,
                headers={"Authorization": f"Bearer {user_token}"},
            )
            assert task2.status_code == status.HTTP_201_CREATED
            task2_id = task2.json()["id"]

        # IMPORTANT: force SQLAlchemy to flush and  reload relationships from the DB
        await dbsession.flush()
        dbsession.expire_all()

        # 3. User submits the challenge (this creates challenge + task histories)
        with patch.object(ConferenceService, "get_raw", new=AsyncMock(return_value=mock_conference)):
            submit_url = fastapi_app.url_path_for("submit_challenge_route", id=challenge_id)
            submit_resp = await client.put(
                submit_url,
                headers={"Authorization": f"Bearer {user_token}"},
            )

            assert submit_resp.status_code == status.HTTP_200_OK

        # 4. User downloads the challenge
        download_url = fastapi_app.url_path_for("download_challenge_document_route", id=challenge_id)
        download_resp = await client.get(
            download_url,
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert download_resp.status_code == status.HTTP_200_OK
        assert download_resp.headers["content-type"] == "application/pdf"
        assert challenge_payload["challenge_name"].replace(" ", "_") in download_resp.headers["x-content-filename"]
        assert download_resp.content.startswith(b"%PDF-1.4")

        # 5. Admin changes challenge status to MinorRevisionRequired
        url = fastapi_app.url_path_for("update_challenge_status_route_admin", id=challenge_id)
        response = await client.put(
            url,
            json={"challenge_status": "MinorRevisionRequired"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["challenge_status"] == "MinorRevisionRequired"

        # 6. User updates challenge
        with patch.object(ConferenceService, "get_raw", new=AsyncMock(return_value=mock_conference)):
            challenge_update_payload = {
                "challenge_name": "Submit Challenge Updated",
                "challenge_abstract": "End-to-end submit test updated",
            }
            update_ch_url = fastapi_app.url_path_for("update_challenge_route", id=challenge_id)
            update_ch_response = await client.put(
                update_ch_url, json=challenge_update_payload, headers={"Authorization": f"Bearer {user_token}"}
            )
        assert update_ch_response.status_code == status.HTTP_200_OK
        assert update_ch_response.json()["challenge_name"] == challenge_update_payload["challenge_name"]
        assert update_ch_response.json()["challenge_abstract"] == challenge_update_payload["challenge_abstract"]

        # 7. User updates tasks

        with patch.object(TaskService, "get_raw", new=get_raw_once):
            task1_update_payload = {"task_name": "Task 1 updated", "task_abstract": "First task updated"}
            update_url = fastapi_app.url_path_for("update_task_route", id=task1_id)
            update_tsk_response = await client.put(
                update_url, json=task1_update_payload, headers={"Authorization": f"Bearer {user_token}"}
            )
            assert update_tsk_response.status_code == status.HTTP_200_OK
            assert update_tsk_response.json()["task_name"] == task1_update_payload["task_name"]
            assert update_tsk_response.json()["task_abstract"] == task1_update_payload["task_abstract"]

        with patch.object(TaskService, "get_raw", new=get_raw_once):
            task2_update_payload = {"task_name": "Task 2 updated", "task_abstract": "First task updated"}
            update_url = fastapi_app.url_path_for("update_task_route", id=task2_id)
            update_tsk2_response = await client.put(
                update_url, json=task2_update_payload, headers={"Authorization": f"Bearer {user_token}"}
            )

            assert update_tsk2_response.status_code == status.HTTP_200_OK
            assert update_tsk2_response.json()["task_name"] == task2_update_payload["task_name"]
            assert update_tsk2_response.json()["task_abstract"] == task2_update_payload["task_abstract"]

        # 8. User submits the revised challenge
        with patch.object(ConferenceService, "get_raw", new=AsyncMock(return_value=mock_conference)):
            submit_url = fastapi_app.url_path_for("submit_challenge_route", id=challenge_id)
            submit_resp = await client.put(
                submit_url,
                headers={"Authorization": f"Bearer {user_token}"},
            )

            assert submit_resp.status_code == status.HTTP_200_OK

        # 9. User downloads the revised challenge
        download_url = fastapi_app.url_path_for("download_challenge_document_route", id=challenge_id)
        download_resp = await client.get(
            download_url,
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert download_resp.status_code == status.HTTP_200_OK
        assert download_resp.headers["content-type"] == "application/pdf"
        assert (
            challenge_update_payload["challenge_name"].replace(" ", "_") in download_resp.headers["x-content-filename"]
        )
        assert download_resp.content.startswith(b"%PDF-1.4")
