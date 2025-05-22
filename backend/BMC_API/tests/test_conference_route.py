# backend/BMC_API/tests/test_conference_route.py
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
class TestConferenceRoutes:
    async def test_user_can_get_open_conferences(self, client: AsyncClient, fastapi_app: FastAPI, admin_token):
        # 1. Create a conference with admin rights for testing, because only admins can create conference.
        url = fastapi_app.url_path_for("create_conference_route_admin")

        response = await client.post(url, json=conference_data, headers={"Authorization": f"Bearer {admin_token}"})

        assert response.status_code == status.HTTP_201_CREATED

        # 2. Test if anyone can access public conference list without any token
        url = fastapi_app.url_path_for("get_all_conferences_limited_route")
        response = await client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "total_pages" in response.json()
        assert "content" in response.json()

    async def test_user_can_get_no_open_conferences(self, client: AsyncClient, fastapi_app: FastAPI):
        url = fastapi_app.url_path_for("get_all_conferences_limited_route")
        response = await client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
