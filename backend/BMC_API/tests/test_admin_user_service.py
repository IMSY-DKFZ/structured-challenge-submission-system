# backend/BMC_API/tests/test_admin_service.py
from datetime import datetime
from unittest.mock import MagicMock

import pytest

from BMC_API.src.api.dependencies.schemas import BulkOperationResponse
from BMC_API.src.application.dto.user_dto import (
    UserCreateAdminDTO,
    UserResponseAdminDTO,
)
from BMC_API.src.core.exceptions import UserAlreadyExistsException
from BMC_API.src.domain.entities.user_model import UserModel

pytest_plugins = ["BMC_API.tests.fixtures.admin_user_fixtures"]


@pytest.mark.anyio
async def test_create_user_success(admin_service, mock_repository):
    # Arrange
    user_create = UserCreateAdminDTO(
        email="test@example.com", password="StrongP@ssword658!", first_name="John", last_name="Doe"
    )

    mock_repository.get_by_email.return_value = None  # No existing user
    user_model = UserModel.create_new(**user_create.model_dump())
    user_model.id = 1  # Set mock ID
    mock_repository.create_obj.return_value = user_model

    background_tasks = MagicMock()

    # Act
    result = await admin_service.create_user(background_tasks=background_tasks, user_create=user_create)

    # Assert
    assert isinstance(result, UserResponseAdminDTO)
    assert result.email == user_create.email.lower()
    mock_repository.get_by_email.assert_awaited_once_with(user_create.email)


@pytest.mark.anyio
async def test_create_user_already_exists(admin_service, mock_repository):
    # Arrange
    user_create = UserCreateAdminDTO(
        email="existing@example.com", password="StrongP@ssword658!", first_name="Jane", last_name="Smith"
    )
    mock_repository.get_by_email.return_value = UserModel()

    # Act / Assert
    with pytest.raises(UserAlreadyExistsException):
        await admin_service.create_user(background_tasks=MagicMock(), user_create=user_create)


@pytest.mark.anyio
def test_create_user_invalid_password():
    # Act / Assert
    with pytest.raises(ValueError) as exc_info:
        UserCreateAdminDTO(
            email="badpass@example.com",
            password="123",  # Invalid password
            first_name="Weak",
            last_name="Password",
        )

    assert "following problem(s) found with the password" in str(exc_info.value).lower()


@pytest.mark.anyio
async def test_update_user_success(admin_service, mock_repository):
    # Arrange
    user_id = 1
    update_data = {"first_name": "Updated", "password": "AnotherS@fePass1!"}

    mock_repository.get.return_value = UserModel(id=user_id, email="user@domain.com", password="old")
    mock_repository.update.return_value = UserModel(id=user_id, email="user@domain.com", **update_data)

    # Act
    result = await admin_service.update(id=user_id, user_update=update_data)

    # Assert
    assert isinstance(result, UserResponseAdminDTO)
    assert result.first_name == update_data["first_name"]
    mock_repository.get.assert_awaited_once_with(id=user_id)
    mock_repository.update.assert_awaited_once()


@pytest.mark.anyio
async def test_update_user_not_found(admin_service, mock_repository):
    # Arrange
    mock_repository.get.return_value = None

    # Act / Assert
    with pytest.raises(Exception) as exc_info:
        await admin_service.update(id=123, user_update={"first_name": "Test"})
    assert "not found" in str(exc_info.value).lower()


@pytest.mark.anyio
async def test_update_no_id(admin_service):
    # Arrange
    update_data = {"first_name": "NewName"}

    # Act / Assert
    with pytest.raises(ValueError) as exc_info:
        await admin_service.update(id=None, user_update=update_data)

    assert "id must be provided" in str(exc_info.value).lower()


@pytest.mark.anyio
async def test_update_not_existing_entity(admin_service, mock_repository):
    # Arrange
    user_id = 9999
    update_data = {"first_name": "Ghost"}
    mock_repository.get.return_value = None

    # Act / Assert
    with pytest.raises(Exception) as exc_info:
        await admin_service.update(id=user_id, user_update=update_data)

    assert "not found for update" in str(exc_info.value).lower()
    mock_repository.get.assert_awaited_once_with(id=user_id)


@pytest.mark.anyio
async def test_update_invalid_password(admin_service, mock_repository):
    # Arrange
    user_id = 42
    update_data = {
        "first_name": "InvalidPass",
        "password": "abc",  # clearly invalid per validation rules
    }

    mock_repository.get.return_value = UserModel(id=user_id, email="test@invalid.com")

    # Act / Assert
    with pytest.raises(Exception) as exc_info:
        await admin_service.update(id=user_id, user_update=update_data)

    assert "password" in str(exc_info.value).lower()


@pytest.mark.anyio
async def test_update_bulk_success(admin_service, mock_repository):
    # Arrange
    updates = [
        {"id": 1, "first_name": "Updated1"},
        {"id": 2, "first_name": "Updated2"},
    ]

    # Simulate both users exist
    mock_repository.get.side_effect = [
        UserModel(id=1, email="u1@example.com", created_time=datetime.now(), modified_time=datetime.now()),
        UserModel(id=2, email="u2@example.com", created_time=datetime.now(), modified_time=datetime.now()),
    ]

    # Simulate update results
    mock_repository.update.side_effect = [
        UserModel(
            id=1,
            first_name="Updated1",
            email="u1@example.com",
            created_time=datetime.now(),
            modified_time=datetime.now(),
        ),
        UserModel(
            id=2,
            first_name="Updated2",
            email="u2@example.com",
            created_time=datetime.now(),
            modified_time=datetime.now(),
        ),
    ]

    # Act
    response: BulkOperationResponse = await admin_service.update_bulk(updates)

    # Assert
    assert len(response.successful) == 2
    assert response.failed == []
    assert response.detail.startswith("Bulk update completed")


@pytest.mark.anyio
async def test_update_bulk_missing_id(admin_service, mock_repository):
    # Arrange
    updates = [{"first_name": "Missing ID"}]  # No 'id'

    # Act
    result: BulkOperationResponse = await admin_service.update_bulk(updates)

    # Assert
    assert len(result.successful) == 0
    assert len(result.failed) == 1
    assert f"Missing {mock_repository.__name__} id" in result.failed[0]["error"]


@pytest.mark.anyio
async def test_update_bulk_user_not_found(admin_service, mock_repository):
    # Arrange
    updates = [{"id": 999, "first_name": "Ghost"}]

    mock_repository.get.return_value = None  # Simulate user not found

    # Act
    result: BulkOperationResponse = await admin_service.update_bulk(updates)

    # Assert
    assert len(result.successful) == 0
    assert len(result.failed) == 1
    assert "not found" in result.failed[0]["error"].lower()
