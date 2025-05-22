# backend/BMC_API/tests/test_admin_route.py

import json

import pytest
from fastapi import HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_503_SERVICE_UNAVAILABLE,
)

from BMC_API.src.api.routes.admin import admin_database


@pytest.mark.anyio
async def test_database_backup_and_download_default_name(tmp_path, monkeypatch):
    # Arrange: create a dummy backup file
    backup_file = tmp_path / "db.sqlite3"
    backup_file.write_text("dummy data")

    async def stub_backup_database(file_name):
        return str(backup_file)

    monkeypatch.setattr(admin_database, "backup_database", stub_backup_database)

    # Act
    response = await admin_database.database_backup_and_download()

    # Assert
    assert isinstance(response, FileResponse)
    assert response.filename == "db.sqlite3"
    assert response.media_type == "application/octet-stream"
    assert response.path == str(backup_file)

@pytest.mark.anyio
async def test_database_backup_and_download_custom_name_added_ext(tmp_path, monkeypatch):
    backup_file = tmp_path / "dump.sqlite3"
    backup_file.write_text("dummy")

    async def stub_backup_database(file_name):
        return str(backup_file)

    monkeypatch.setattr(admin_database, "backup_database", stub_backup_database)

    response = await admin_database.database_backup_and_download("backup")
    assert response.filename == "backup.sqlite3"

@pytest.mark.anyio
async def test_database_backup_and_download_custom_name_with_ext(tmp_path, monkeypatch):
    backup_file = tmp_path / "dump.sqlite3"
    backup_file.write_text("dummy")

    async def stub_backup_database(file_name):
        return str(backup_file)

    monkeypatch.setattr(admin_database, "backup_database", stub_backup_database)

    response = await admin_database.database_backup_and_download("custom.sqlite3")
    assert response.filename == "custom.sqlite3"

@pytest.mark.anyio
async def test_database_backup_and_download_runtime_error(monkeypatch):
    async def stub_backup_database(file_name):
        raise RuntimeError("failed")

    monkeypatch.setattr(admin_database, "backup_database", stub_backup_database)

    with pytest.raises(HTTPException) as exc_info:
        await admin_database.database_backup_and_download()
    assert exc_info.value.status_code == HTTP_503_SERVICE_UNAVAILABLE
    assert "Something went wrong" in exc_info.value.detail

@pytest.mark.anyio
async def test_database_backup_and_download_file_not_found(monkeypatch):
    async def stub_backup_database(file_name):
        raise FileNotFoundError("not found")

    monkeypatch.setattr(admin_database, "backup_database", stub_backup_database)

    with pytest.raises(HTTPException) as exc_info:
        await admin_database.database_backup_and_download()
    assert exc_info.value.status_code == HTTP_404_NOT_FOUND

@pytest.mark.anyio
async def test_database_backup_and_download_generic_exception(monkeypatch):
    async def stub_backup_database(file_name):
        raise Exception("error")

    monkeypatch.setattr(admin_database, "backup_database", stub_backup_database)

    with pytest.raises(HTTPException) as exc_info:
        await admin_database.database_backup_and_download()
    assert exc_info.value.status_code == HTTP_503_SERVICE_UNAVAILABLE


@pytest.mark.anyio
async def test_delete_database_backups_default(monkeypatch):
    async def stub_delete_db_backups(delete_all: bool):
        return ["a", "b"]

    monkeypatch.setattr(admin_database, "delete_db_backups", stub_delete_db_backups)

    # current_active_user is not used in logic; pass None
    response = await admin_database.delete_database_backups(current_active_user=None, delete_all_backups=False)
    assert isinstance(response, JSONResponse)
    assert response.status_code == HTTP_200_OK
    data = json.loads(response.body)
    assert data["message"] == "All database backups except the latest one successfully deleted."
    assert data["deleted_files"] == ["a", "b"]

@pytest.mark.anyio
async def test_delete_database_backups_delete_all(monkeypatch):
    async def stub_delete_db_backups(delete_all: bool):
        return ["x", "y", "z"]

    monkeypatch.setattr(admin_database, "delete_db_backups", stub_delete_db_backups)

    response = await admin_database.delete_database_backups(current_active_user=None, delete_all_backups=True)
    data = json.loads(response.body)
    assert data["message"] == "All database backups successfully deleted."
    assert data["deleted_files"] == ["x", "y", "z"]

@pytest.mark.anyio
async def test_delete_database_backups_exception(monkeypatch):
    async def stub_delete_db_backups(delete_all: bool):
        raise Exception("oops")

    monkeypatch.setattr(admin_database, "delete_db_backups", stub_delete_db_backups)

    with pytest.raises(HTTPException) as exc_info:
        await admin_database.delete_database_backups(current_active_user=None, delete_all_backups=False)
    assert exc_info.value.status_code == HTTP_503_SERVICE_UNAVAILABLE


@pytest.mark.anyio
async def test_backup_endpoint_via_client(tmp_path, monkeypatch, client, fastapi_app):
    """
    Integration test: POST /database_backup_and_download returns the file and correct headers
    """

    # Create a dummy backup
    backup_file = tmp_path / "endpoint.sqlite3"
    backup_file.write_text("hello world")

    async def stub_backup_database(file_name):
        return str(backup_file)

    # Patch the database backup call
    monkeypatch.setattr(admin_database, "backup_database", stub_backup_database)
    # Bypass RoleChecker by no-oping its __call__
    monkeypatch.setattr(admin_database.RoleChecker, "__call__", lambda self: None)

    # Request without file_name param
    url = fastapi_app.url_path_for("database_backup_and_download")
    response = await client.post(url)
    assert response.status_code == status.HTTP_200_OK
    # Should attach the file with correct filename
    assert response.headers["content-disposition"] == 'attachment; filename="endpoint.sqlite3"'
    assert response.content == b"hello world"

@pytest.mark.anyio
async def test_delete_backups_endpoint_via_client(monkeypatch, client, fastapi_app):
    """
    Integration test: DELETE /delete_database_backups returns JSON
    """

    async def stub_delete_db_backups(delete_all: bool):
        return ["old1", "old2"]

    monkeypatch.setattr(admin_database, "delete_db_backups", stub_delete_db_backups)
    # Bypass RoleChecker
    monkeypatch.setattr(admin_database.RoleChecker, "__call__", lambda self: None)
    # Bypass password check dependency
    fastapi_app.dependency_overrides[admin_database.validate_active_user_password_dependency] = lambda: None

    url = fastapi_app.url_path_for("delete_database_backups")
    response = await client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data == {
        "message": "All database backups except the latest one successfully deleted.",
        "deleted_files": ["old1", "old2"],
    }
