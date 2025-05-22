
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from BMC_API.src.api.routes import contact
from BMC_API.src.core.exceptions import NotFoundException


@pytest.fixture
def mock_contact_dependencies(fastapi_app):
    mock_user_service = MagicMock()
    mock_user_service.list = AsyncMock()

    mock_conference_service = MagicMock()
    mock_conference_service.list = AsyncMock()

    mock_scheduler = MagicMock()
    mock_scheduler.schedule_contact_message = MagicMock()

    fastapi_app.dependency_overrides[contact.user_service_dependency] = lambda: mock_user_service
    fastapi_app.dependency_overrides[contact.conference_service_dependency] = lambda: mock_conference_service
    contact.EmailSchedulerService = lambda bg: mock_scheduler

    return {
        "user_service": mock_user_service,
        "conference_service": mock_conference_service,
        "email_scheduler": mock_scheduler,
    }

@pytest.mark.anyio
async def test_send_to_challenge_chairs(client, fastapi_app, mock_contact_dependencies):
    mock_conference = MagicMock()
    mock_conference.chairperson_emails = ["chair1@example.com", "chair2@example.com"]
    mock_contact_dependencies["conference_service"].list.return_value = [mock_conference]

    url = fastapi_app.url_path_for("send_message")
    data = {
        "subject": "Sync Request",
        "message": "Please update submission deadlines.",
        "recipients_group": "Challenge chairs",
        "sender_name": "Alice",
        "sender_email": "alice@example.com"
    }

    response = await client.post(url, json=data)

    assert response.status_code == 200
    assert response.json()["message"] == "Your message has been sent successfully."
    mock_contact_dependencies["email_scheduler"].schedule_contact_message.assert_called_once()


@pytest.mark.anyio
async def test_send_to_technical_support(client, fastapi_app, mock_contact_dependencies):
    admin_mock = MagicMock()
    admin_mock.email = "admin@example.com"
    mock_contact_dependencies["user_service"].list.return_value = [admin_mock]

    url = fastapi_app.url_path_for("send_message")
    data = {
        "subject": "Help Needed",
        "message": "Can't access my submission.",
        "recipients_group": "Technical support",
        "sender_name": "Bob",
        "sender_email": "bob@example.com"
    }

    response = await client.post(url, json=data)

    assert response.status_code == 200
    assert response.json()["message"] == "Your message has been sent successfully."
    mock_contact_dependencies["email_scheduler"].schedule_contact_message.assert_called_once()


@pytest.mark.anyio
async def test_invalid_recipients_group(client: AsyncClient, fastapi_app: FastAPI):
    url = fastapi_app.url_path_for("send_message")
    message_data = {
        "subject": "Invalid Group Test",
        "message": "Should fail validation",
        "recipients_group": "Martians",
        "sender_name": "Fake User",
        "sender_email": "fake@example.com"
    }

    response = await client.post(url, json=message_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"] == "Invalid recipient type"


@pytest.mark.anyio
async def test_no_open_conferences(client, fastapi_app, mock_contact_dependencies):
    mock_contact_dependencies["conference_service"].list.side_effect = NotFoundException

    url = fastapi_app.url_path_for("send_message")
    data = {
        "subject": "No Conferences",
        "message": "Test when no open conferences exist.",
        "recipients_group": "Challenge chairs",
        "sender_name": "Carl Confused",
        "sender_email": "carl@example.com"
    }

    response = await client.post(url, json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No active conference found."


@pytest.mark.anyio
async def test_string_admin_list(client, fastapi_app, mock_contact_dependencies):
    admin_mock = MagicMock()
    admin_mock.email = "admin@example.com"
    mock_contact_dependencies["user_service"].list.return_value = [admin_mock]

    url = fastapi_app.url_path_for("send_message")
    data = {
        "subject": "String Admin",
        "message": "Edge case with string list return",
        "recipients_group": "Technical support",
        "sender_name": "Test User",
        "sender_email": "testuser@example.com"
    }

    response = await client.post(url, json=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Your message has been sent successfully."


# Schema validation tests


@pytest.mark.anyio
@pytest.mark.parametrize("payload,missing_field", [
    ({
        "subject": "Hi",
        "recipients_group": "Challenge chairs",
        "sender_name": "John",
        "sender_email": "valid@example.com"
    }, "message"),

    ({
        "message": "Hello",
        "subject": "Hi",
        "sender_name": "John",
        "sender_email": "valid@example.com"
    }, "recipients_group"),

    ({
        "message": "Hello",
        "subject": "Hi",
        "recipients_group": "Challenge chairs",
        "sender_name": "John"
    }, "sender_email"),
])
async def test_missing_required_fields(payload, missing_field, client, fastapi_app):
    url = fastapi_app.url_path_for("send_message")
    response = await client.post(url, json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert any(missing_field in err["loc"] for err in response.json()["detail"])



@pytest.mark.anyio
async def test_invalid_email_format(client: AsyncClient, fastapi_app: FastAPI):
    payload = {
        "message": "Test",
        "subject": "Email Test",
        "recipients_group": "Challenge chairs",
        "sender_name": "NotAnEmail",
        "sender_email": "not-an-email"
    }

    url = fastapi_app.url_path_for("send_message")
    response = await client.post(url, json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert any("sender_email" in err["loc"] for err in response.json()["detail"])
