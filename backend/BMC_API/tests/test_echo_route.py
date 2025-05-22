# backend/BMC_API/tests/test_echo_route.py
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from BMC_API.src.api.schemas.echo_schema import Message


@pytest.mark.anyio
async def test_monitoring(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Checks the echo endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    message = Message(message="This is a test message").model_dump()
    url = fastapi_app.url_path_for("send_echo_message")
    response = await client.post(url, json=message)
    assert response.status_code == status.HTTP_200_OK
