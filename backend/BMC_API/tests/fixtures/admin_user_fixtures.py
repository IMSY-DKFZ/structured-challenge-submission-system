# backend/BMC_API/tests/fixtures/admin_user_fixtures.py
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

# from pydantic import EmailStr
from BMC_API.src.application.dto.user_dto import (
    UserCreateAdminDTO,
    UserResponseAdminDTO,
    UserUpdateAdminDTO,
)
from BMC_API.src.application.use_cases.admin_use_cases import AdminUserService
from BMC_API.src.domain.entities.user_model import UserModel

# from BMC_API.src.application.use_cases.user_use_cases import UserService
from BMC_API.src.domain.value_objects.enums.user_enums import Roles


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def mock_token_cache():
    return MagicMock()


@pytest.fixture
def admin_service(mock_repository, mock_token_cache):
    return AdminUserService(repository=mock_repository, dto_class=UserResponseAdminDTO, token_cache=mock_token_cache)


# Arrange a test admin
@pytest.fixture(scope="session")
def test_admin():
    return UserCreateAdminDTO(
        email="admin@example.com",
        password="AdminUser1#",
        first_name="Test",
        last_name="Admin",
        city="",
        country="",
        institution="",
        email_confirmed=True,
        roles=[Roles.ADMIN],
    )


# Arrange a e-mail confirmed, active, non-disabled test user
@pytest.fixture
def test_user_confirmed():
    return UserCreateAdminDTO(
        email="test@example.com",
        password="Mypassword1#",
        first_name="test",
        last_name="test",
        city="",
        country="",
        institution="",
        email_confirmed=True,
        roles=[Roles.ORGANIZER],
    )


@pytest.fixture
def test_admin_create_dto():
    """Fixture for creating an admin user DTO"""
    return UserCreateAdminDTO(
        email="admin_create@example.com",
        password="AdminPass1#",
        first_name="Admin",
        last_name="Creator",
        city="Admin City",
        country="Admin Country",
        institution="Admin Institute",
        roles=[Roles.ADMIN],
        disabled=False,
        email_confirmed=True,
    )


@pytest.fixture
def test_user_admin_create_dto():
    """Fixture for creating a regular user via admin DTO"""
    return UserCreateAdminDTO(
        email="user_via_admin@example.com",
        password="UserPass1#",
        first_name="Regular",
        last_name="User",
        city="User City",
        country="User Country",
        institution="User Institute",
        roles=[Roles.ORGANIZER],
        disabled=False,
        email_confirmed=True,
    )


@pytest.fixture
def test_user_update_admin_dto():
    """Fixture for updating a user via admin DTO"""
    return UserUpdateAdminDTO(
        email="updated_user@example.com",
        first_name="Updated",
        last_name="User",
        city="Updated City",
        country="Updated Country",
        institution="Updated Institute",
        roles=[Roles.ORGANIZER],
        disabled=False,
    )


@pytest.fixture
def test_bulk_update_data():
    """Fixture for bulk updating users"""
    return [
        {"id": 1, "first_name": "Bulk", "last_name": "Update1"},
        {"id": 2, "first_name": "Bulk", "last_name": "Update2"},
    ]


@pytest.fixture
async def test_admin_login(fastapi_app, client, dbsession, test_admin):
    """Creates admin directly in DB and returns login function"""

    from BMC_API.src.application.interfaces.password_hasher_impl import (
        BcryptPasswordHasher,
    )

    # Insert admin directly in the database
    password_hasher = BcryptPasswordHasher()
    hashed_password = password_hasher.hash(test_admin.password)

    user_data = test_admin.model_dump()
    user_data["password"] = hashed_password

    admin_user = UserModel(**user_data)
    admin_user.created_time = datetime.now()
    admin_user.modified_time = datetime.now()

    dbsession.add(admin_user)
    await dbsession.commit()
    await dbsession.refresh(admin_user)

    # Define login function to get token
    async def _get_admin_token():
        login_data = {"username": test_admin.email, "password": test_admin.password}
        login_url = fastapi_app.url_path_for("login_route")
        login_response = await client.post(login_url, data=login_data)
        return login_response.json()["access_token"]

    return _get_admin_token


@pytest.fixture
async def admin_token(test_admin_login):
    """Returns an access token for the admin user."""
    return await test_admin_login()
