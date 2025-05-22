# backend/BMC_API/tests/test_admin_conference_route.py
from copy import deepcopy

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

pytest_plugins = [
    "BMC_API.tests.fixtures.admin_user_fixtures",
    "BMC_API.tests.fixtures.user_fixtures",
]

conference_data = {
    "name": "Test Conference",
    "short_name": "Tst2025",
    "information": "Test Conference",
    "proposal_start_date": "2030-12-31T23:59:59",
    "proposal_end_date": "2031-01-15T23:59:59",
    "start_date": "2030-12-31T23:59:59",
    "end_date": "2031-01-15T23:59:59",
    "city": "City",
    "venue": "Venue",
    "country": "Country",
    "year": 2025,
    "is_open_for_submissions": True,
    "chairperson_names": ["chair1", "chair2"],
    "chairperson_emails": ["chair1@example.com", "chair2@example.com"],
}


@pytest.mark.anyio
class TestAdminConferenceRoutes:
    async def test_admin_can_create_conference(self, client: AsyncClient, fastapi_app: FastAPI, admin_token):
        url = fastapi_app.url_path_for("create_conference_route_admin")

        response = await client.post(url, json=conference_data, headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == conference_data["name"]

    async def test_admin_can_get_conference_by_id(self, client: AsyncClient, fastapi_app: FastAPI, admin_token):
        # First create a conference
        create_url = fastapi_app.url_path_for("create_conference_route_admin")

        create_resp = await client.post(
            create_url, json=conference_data, headers={"Authorization": f"Bearer {admin_token}"}
        )
        conf_id = create_resp.json()["id"]

        get_url = fastapi_app.url_path_for("get_conference_route_admin", id=conf_id)
        response = await client.get(get_url, headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == conf_id

    async def test_admin_can_get_all_conferences(self, client: AsyncClient, fastapi_app: FastAPI, admin_token):
        # First create a conference
        create_url = fastapi_app.url_path_for("create_conference_route_admin")
        data = deepcopy(conference_data)
        response = await client.post(create_url, json=data, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == status.HTTP_201_CREATED

        data["name"] = "Bulk 2"
        data["chairperson_emails"] = ["bulk2@example.com"]
        response = await client.post(create_url, json=data, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == status.HTTP_201_CREATED

        get_url = fastapi_app.url_path_for("list_conferences_route_admin")
        response = await client.post(get_url, headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["total_pages"] == 1
        assert response.json()["total_records"] == 2
        assert len(response.json()["content"]) == 2
        assert response.json()["content"][0]["name"] == conference_data["name"]
        assert response.json()["content"][1]["name"] == data["name"]

    async def test_admin_can_update_conference(self, client: AsyncClient, fastapi_app: FastAPI, admin_token):
        # Create a conference
        create_url = fastapi_app.url_path_for("create_conference_route_admin")
        create_resp = await client.post(
            create_url, json=conference_data, headers={"Authorization": f"Bearer {admin_token}"}
        )
        conf_id = create_resp.json()["id"]

        # Update
        update_data = {
            "name": "Updated Name",
            "venue": "Hybrid",
        }

        update_url = fastapi_app.url_path_for("update_conference_route_admin", id=conf_id)
        response = await client.put(update_url, json=update_data, headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == update_data["name"]
        assert response.json()["venue"] == update_data["venue"]

    async def test_admin_can_bulk_update_conferences(self, client: AsyncClient, fastapi_app: FastAPI, admin_token):
        create_url = fastapi_app.url_path_for("create_conference_route_admin")
        data = deepcopy(conference_data)
        resp1 = await client.post(create_url, json=data, headers={"Authorization": f"Bearer {admin_token}"})
        conf_id1 = resp1.json()["id"]

        data["name"] = "Bulk 2"
        data["chairperson_emails"] = ["bulk2@example.com"]
        resp2 = await client.post(create_url, json=data, headers={"Authorization": f"Bearer {admin_token}"})
        conf_id2 = resp2.json()["id"]

        bulk_update_url = fastapi_app.url_path_for("bulk_update_conferences_route_admin")
        updates = [
            {"id": conf_id1, "venue": "On-site"},
            {"id": conf_id2, "venue": "Remote"},
        ]

        response = await client.put(bulk_update_url, json=updates, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == status.HTTP_200_OK
        assert "Bulk update completed" in response.json()["detail"]
        assert len(response.json()["successful"]) == 2
        assert response.json()["successful"][0]["name"] == conference_data["name"]
        assert response.json()["successful"][1]["name"] == data["name"]
        assert len(response.json()["failed"]) == 0

    async def test_admin_can_delete_conference(
        self, client: AsyncClient, fastapi_app: FastAPI, admin_token, test_admin
    ):
        # Create a conference
        create_url = fastapi_app.url_path_for("create_conference_route_admin")
        create_resp = await client.post(
            create_url, json=conference_data, headers={"Authorization": f"Bearer {admin_token}"}
        )
        conf_id = create_resp.json()["id"]

        delete_url = fastapi_app.url_path_for("delete_conference_route_admin", id=conf_id)
        response = await client.delete(
            delete_url,
            params={"active_user_password": test_admin.password},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["detail"] == "Conference deleted"

    async def test_admin_can_bulk_delete_conferences(
        self, client: AsyncClient, fastapi_app: FastAPI, admin_token, test_admin
    ):
        create_url = fastapi_app.url_path_for("create_conference_route_admin")
        data = deepcopy(conference_data)
        resp1 = await client.post(create_url, json=data, headers={"Authorization": f"Bearer {admin_token}"})

        data["name"] = "Bulk 2"
        resp2 = await client.post(create_url, json=data, headers={"Authorization": f"Bearer {admin_token}"})
        ids = [resp1.json()["id"], resp2.json()["id"]]

        bulk_delete_url = fastapi_app.url_path_for("bulk_delete_conferences_route_admin")
        # response = await client.delete(bulk_delete_url, params={"active_user_password": test_admin.password}, json=ids, headers={"Authorization": f"Bearer {admin_token}"})
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
