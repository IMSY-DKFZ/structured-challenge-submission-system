# backend/BMC_API/tests/fixtures/user_fixtures.py

import pytest

from BMC_API.src.application.dto.user_dto import UserCreateDTO
from BMC_API.src.domain.entities.user_model import UserModel


# Arrange a test user
@pytest.fixture
def test_user():
    return UserCreateDTO(
        email="test@example.com",
        password="Mypassword1#",
        first_name="test",
        last_name="test",
        city="",
        country="",
        institution="",
    )


# Arrange a test user
@pytest.fixture
def test_user2():
    return UserCreateDTO(
        email="test2@example.com",
        password="Mypassword1#",
        first_name="test 2",
        last_name="test 2",
        city="",
        country="",
        institution="",
    )


@pytest.fixture
def confirmed_user(monkeypatch):
    """
    Fixture to patch UserModel.create_new so that users are created with email_confirmed=True.
    """
    original_create_new = UserModel.create_new

    def confirmed_create_new(email: str, password: str, first_name: str, last_name: str, **kwargs):
        user = original_create_new(email, password, first_name, last_name, **kwargs)
        user.email_confirmed = True
        user.email_confirmation_token = None
        return user

    monkeypatch.setattr(UserModel, "create_new", confirmed_create_new)


# @pytest.fixture
# async def test_user_login(fastapi_app, client, dbsession, test_user, confirmed_user):
#     """Creates admin directly in DB and returns login function"""

#     from BMC_API.src.application.interfaces.password_hasher_impl import (
#         BcryptPasswordHasher,
#     )

#     # Insert user directly in the database
#     password_hasher = BcryptPasswordHasher()
#     hashed_password = password_hasher.hash(test_user.password)

#     user_data = test_user.model_dump()
#     user_data["password"] = hashed_password

#     user = UserModel.create_new(**user_data)

#     dbsession.add(user)
#     await dbsession.commit()
#     await dbsession.refresh(user)

#     # Define login function to get token
#     async def _get_user_token():
#         login_data = {"username": test_user.email, "password": test_user.password}
#         login_url = fastapi_app.url_path_for("login_route")
#         login_response = await client.post(login_url, data=login_data)
#         return login_response.json()["access_token"]

#     return _get_user_token


@pytest.fixture
async def user_token(login_user_factory, test_user):
    """Returns an access token for the normal user."""
    return await login_user_factory(test_user)


# @pytest.fixture
# def override_admin_auth(fastapi_app: FastAPI):
#     """
#     Overrides the authentication dependency to always return a fake admin user.
#     """
#     fake_admin = UserInDB(
#         id=1,
#         email="admin@example.com",
#         first_name="Admin",
#         last_name="User",
#         roles=[Roles.ADMIN],
#     )

#     async def override_get_current_user_dependency():
#         return fake_admin

#     async def override_get_current_active_user_dependency():
#         return fake_admin

#     async def override_validate_current_access_token_dependency():
#         # Return a dummy token without any validation.
#         return "dummy_token"

#     fastapi_app.dependency_overrides[validate_current_access_token_dependency] = (
#         override_validate_current_access_token_dependency
#     )
#     fastapi_app.dependency_overrides[get_current_user_dependency] = (
#         override_get_current_user_dependency
#     )
#     fastapi_app.dependency_overrides[get_current_active_user_dependency] = (
#         override_get_current_active_user_dependency
#     )
#     yield
#     fastapi_app.dependency_overrides.pop(validate_current_access_token_dependency, None)
#     fastapi_app.dependency_overrides.pop(get_current_user_dependency, None)
#     fastapi_app.dependency_overrides.pop(get_current_active_user_dependency, None)


# # Arrange a test admin taken from database
# @pytest.fixture(scope="session")
# def test_admin_in_db():
#     return pytest.test_admin_in_db


# # Arrange test admin token
# @pytest.fixture(scope="session")
# def test_admin_token():
#     return pytest.test_admin_token
