# backend/BMC_API/tests/test_user_route.py


from copy import deepcopy
from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from BMC_API.src.application.dto.user_dto import UserCreateDTO
from BMC_API.src.domain.entities.user_model import UserModel

pytest_plugins = [
    "BMC_API.tests.fixtures.user_fixtures",
]


@pytest.mark.anyio
class TestUserRoutes:
    async def test_create_user_success(self, client: AsyncClient, test_user: UserCreateDTO, fastapi_app: FastAPI):
        # Arrange
        user_data = test_user.model_dump()

        # Act
        url = fastapi_app.url_path_for("create_user_route")
        response = await client.post(url, json=user_data)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["email"] == test_user.email
        assert response.json()["first_name"] == test_user.first_name
        assert response.json()["last_name"] == test_user.last_name
        assert "password" not in response.json()  # Password should not be returned

    async def test_create_user_duplicate(self, client: AsyncClient, test_user: UserCreateDTO, fastapi_app: FastAPI):
        # Arrange
        user_data = test_user.model_dump()

        # First create the user
        url = fastapi_app.url_path_for("create_user_route")
        response = await client.post(url, json=user_data)

        # Act - Try to create the same user again
        response = await client.post(url, json=user_data)

        # Assert
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "already exists" in response.json()["detail"]

    async def test_create_user_while_logged_in(
        self, client: AsyncClient, test_user: UserCreateDTO, fastapi_app: FastAPI, user_token
    ):
        # Arrange
        user_data = test_user.model_dump()

        # Try to create the user while logged in
        url = fastapi_app.url_path_for("create_user_route")
        response = await client.post(url, json=user_data, headers={"Authorization": f"Bearer {user_token}"})

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Cannot create new account while logged in" in response.json()["detail"]

    async def test_create_user_validation_error(self, client: AsyncClient, fastapi_app: FastAPI):
        # Arrange
        invalid_user_data = {
            "email": "not-an-email",  # Invalid email format
            "password": "short",  # Too short password
            "first_name": "Test",
            "last_name": "User",
        }

        # Act
        url = fastapi_app.url_path_for("create_user_route")
        response = await client.post(url, json=invalid_user_data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # Validation error

    async def test_login_success(
        self,
        client: AsyncClient,
        test_user: UserCreateDTO,
        fastapi_app: FastAPI,
        monkeypatch,
    ):
        # Arrange
        # First create a user
        user_data = test_user.model_dump()

        # Patch the token generation to always return "123456"
        monkeypatch.setattr(UserModel, "generate_confirmation_token", lambda: "123456")

        url = fastapi_app.url_path_for("create_user_route")
        response = await client.post(url, json=user_data)
        assert response.status_code == status.HTTP_201_CREATED

        # Prepare login data
        login_data = {
            "username": test_user.email,  # OAuth2 uses username field, but we send email
            "password": test_user.password,
        }

        # Act
        url = fastapi_app.url_path_for("login_route")
        response = await client.post(url, data=login_data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email not confirmed. Please verify your email address." in response.json()["detail"]

        # Act
        url = fastapi_app.url_path_for("confirm_email_route")
        response = await client.post(url, params={"confirmation_token": 123456})

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert "Email confirmed successfully." in response.json()["detail"]

        # Act
        url = fastapi_app.url_path_for("login_route")
        response = await client.post(url, data=login_data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    async def test_login_invalid_credentials(
        self,
        client: AsyncClient,
        test_user: UserCreateDTO,
        fastapi_app: FastAPI,
        confirmed_user,
    ):
        # Arrange
        # First create a user
        user_data = test_user.model_dump()

        url = fastapi_app.url_path_for("create_user_route")
        response = await client.post(url, json=user_data)
        assert response.status_code == status.HTTP_201_CREATED

        # Prepare login data with wrong password
        login_data = {"username": test_user.email, "password": "wrong_password"}

        # Act
        url = fastapi_app.url_path_for("login_route")
        response = await client.post(url, data=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Could not validate credentials" in response.json()["detail"]

    async def test_confirm_email(
        self,
        client: AsyncClient,
        test_user: UserCreateDTO,
        fastapi_app: FastAPI,
        monkeypatch,
    ):
        # Arrange
        user_data = test_user.model_dump()
        # Patch the token generation to always return "123456"
        monkeypatch.setattr(UserModel, "generate_confirmation_token", lambda: "123456")

        # Create a user first
        url = fastapi_app.url_path_for("create_user_route")
        create_response = await client.post(url, json=user_data)
        assert create_response.status_code == status.HTTP_201_CREATED

        # Act
        url = fastapi_app.url_path_for("confirm_email_route")
        response = await client.post(url, params={"confirmation_token": 123456})

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert "Email confirmed successfully" in response.json()["detail"]

    async def test_confirm_email_invalid_token(self, client: AsyncClient, fastapi_app: FastAPI):
        # Arrange - Use an invalid token
        invalid_token = "invalid_token"

        # Act
        url = fastapi_app.url_path_for("confirm_email_route")
        response = await client.post(url, params={"confirmation_token": invalid_token})

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid confirmation token" in response.json()["detail"]

    async def test_reset_password_request(self, client: AsyncClient, test_user: UserCreateDTO, fastapi_app: FastAPI):
        # Arrange
        # Create a user first
        user_data = test_user.model_dump()
        url = fastapi_app.url_path_for("create_user_route")
        await client.post(url, json=user_data)

        # Mock the repository's get_by_email method to bypass "email_confirmed" and "disabled" checks
        
        with patch("BMC_API.src.infrastructure.persistence.dao.user_dao.SQLAlchemyUserRepository.get_by_email", new_callable=AsyncMock) as mock_get_by_email:
            from BMC_API.src.domain.entities.user_model import UserModel
            user_obj = UserModel(email="fake@email.com",
                                password="1234",
                                created_time=datetime.now(),
                                email_confirmed=True, 
                                disabled=False)
            mock_get_by_email.return_value = user_obj

            # Act
            url = fastapi_app.url_path_for("reset_password_request_route")
            response = await client.post(url, params={"email": test_user.email})

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert "Password reset instructions" in response.json()["detail"]

    async def test_reset_password_request_nonexistent_user(self, client: AsyncClient, fastapi_app: FastAPI):
        # Arrange
        nonexistent_email = "nonexistent@example.com"

        # Act
        url = fastapi_app.url_path_for("reset_password_request_route")
        response = await client.post(url, params={"email": nonexistent_email})

        # Assert - Should still return status.HTTP_200_OK to avoid leaking information about existing accounts
        assert response.status_code == status.HTTP_200_OK
        assert "Password reset instructions" in response.json()["detail"]

    async def test_reset_password(self, client: AsyncClient, test_user: UserCreateDTO, fastapi_app: FastAPI):
        # Arrange
        # Create a user first
        user_data = test_user.model_dump()
        url = fastapi_app.url_path_for("create_user_route")
        await client.post(url, json=user_data)

        # Request password reset to generate a token
        url = fastapi_app.url_path_for("reset_password_request_route")
        await client.post(url, params={"email": test_user.email})

        # Extract reset token from logs or directly from the database
        # For testing, we'll patch the reset_password method since accessing logs might be complex
        reset_token = "mock_reset_token"
        new_password = "NewSecure9247#"

        with patch("BMC_API.src.infrastructure.persistence.dao.user_dao.SQLAlchemyUserRepository.reset_password"):
            # Act
            url = fastapi_app.url_path_for("reset_password_route")
            response = await client.post(
                url,
                json={"reset_token": reset_token, "new_password": new_password},
            )

            # Assert
            assert response.status_code == status.HTTP_200_OK
            assert "Password reset successfully" in response.json()["detail"]

    async def test_reset_password_invalid_token(self, client: AsyncClient, fastapi_app: FastAPI):
        # Arrange
        invalid_token = "invalid_token"
        new_password = "NewSecure9247#"

        # Act
        url = fastapi_app.url_path_for("reset_password_route")
        response = await client.post(
            url,
            json={"reset_token": invalid_token, "new_password": new_password},
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid reset token" in response.json()["detail"]

    async def test_get_me_authenticated(
        self,
        client: AsyncClient,
        test_user: UserCreateDTO,
        fastapi_app: FastAPI,
        confirmed_user,
    ):
        # Arrange
        # Create the user
        user_data = test_user.model_dump()
        url = fastapi_app.url_path_for("create_user_route")
        await client.post(url, json=user_data)

        # Login to get tokens
        login_data = {"username": test_user.email, "password": test_user.password}
        url = fastapi_app.url_path_for("login_route")
        login_response = await client.post(url, data=login_data)
        token = login_response.json()["access_token"]

        # Act
        url = fastapi_app.url_path_for("read_user_route")
        response = await client.get(url, headers={"Authorization": f"Bearer {token}"})

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == test_user.email
        assert response.json()["first_name"] == test_user.first_name
        assert response.json()["last_name"] == test_user.last_name

    async def test_update_user_success(
        self, client: AsyncClient, fastapi_app: FastAPI, test_user: UserCreateDTO, user_token
    ):
        update_data = deepcopy(test_user.model_dump())
        update_data.pop("password")
        update_data.pop("email")
        update_data["first_name"] = "Updated name"

        # Act
        url = fastapi_app.url_path_for("update_user_route")
        response = await client.put(url, json=update_data, headers={"Authorization": f"Bearer {user_token}"})

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == test_user.model_dump()["email"]
        assert response.json()["first_name"] == update_data["first_name"]
        assert response.json()["last_name"] == test_user.model_dump()["last_name"]
        assert "password" not in response.json()

    async def test_update_user_without_credentials(
        self, client: AsyncClient, fastapi_app: FastAPI, test_user: UserCreateDTO, user_token
    ):
        update_data = deepcopy(test_user.model_dump())
        update_data.pop("password")
        update_data.pop("email")
        update_data["first_name"] = "Updated name"

        # Act
        url = fastapi_app.url_path_for("update_user_route")
        response = await client.put(url, json=update_data)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_log_out_success(
        self, client: AsyncClient, test_user: UserCreateDTO, fastapi_app: FastAPI, dbsession, confirmed_user
    ):
        # Arrange
        from BMC_API.src.application.interfaces.password_hasher_impl import (
            BcryptPasswordHasher,
        )

        password_hasher = BcryptPasswordHasher()
        hashed_password = password_hasher.hash(test_user.password)

        user_data = test_user.model_dump()
        user_data["password"] = hashed_password

        user = UserModel.create_new(**user_data)
        user.created_time = datetime.now()
        user.modified_time = datetime.now()

        dbsession.add(user)
        await dbsession.commit()
        await dbsession.refresh(user)

        login_data = {"username": test_user.email, "password": test_user.password}
        login_url = fastapi_app.url_path_for("login_route")
        login_response = await client.post(login_url, data=login_data)

        assert login_response.status_code == status.HTTP_200_OK
        token_data = login_response.json()

        # Act
        url = fastapi_app.url_path_for("logout_token_route")
        # response = await client.post(url, json=token_data, headers={"Authorization": f"Bearer {user_token}"})
        response = await client.post(url, json=token_data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert "Logged out successfully" in response.json()["detail"]

    async def test_log_out_with_false_token_data(
        self, client: AsyncClient, test_user: UserCreateDTO, fastapi_app: FastAPI, dbsession, confirmed_user
    ):
        # Arrange

        token_data_wrong_format = "Broken data"
        token_data_missing = {"access_token": "Broken data"}
        token_data_boken = {"access_token": "Broken data", "refresh_token": "Broken data"}

        # Act
        url = fastapi_app.url_path_for("logout_token_route")
        response = await client.post(url, json=token_data_wrong_format)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Act
        url = fastapi_app.url_path_for("logout_token_route")
        response = await client.post(url, json=token_data_missing)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Act
        url = fastapi_app.url_path_for("logout_token_route")
        response = await client.post(url, json=token_data_boken)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect token" in response.json()["detail"]

    async def test_refresh_token_success(
        self,
        client: AsyncClient,
        test_user: UserCreateDTO,
        fastapi_app: FastAPI,
        monkeypatch,
        ):
        # Arrange: patch confirmation token to a known value
        monkeypatch.setattr(UserModel, "generate_confirmation_token", lambda: "123456")
        user_data = test_user.model_dump()

        create_url = fastapi_app.url_path_for("create_user_route")
        create_resp = await client.post(create_url, json=user_data)
        assert create_resp.status_code == status.HTTP_201_CREATED

        confirm_url = fastapi_app.url_path_for("confirm_email_route")
        confirm_resp = await client.post(confirm_url, params={"confirmation_token": 123456})
        assert confirm_resp.status_code == status.HTTP_200_OK

        login_data = {"username": test_user.email, "password": test_user.password}
        login_url = fastapi_app.url_path_for("login_route")
        login_resp = await client.post(login_url, data=login_data)
        assert login_resp.status_code == status.HTTP_200_OK
        tokens = login_resp.json()

        # Act: refresh the tokens
        refresh_url = fastapi_app.url_path_for("refresh_token_route")
        response = await client.post(
            refresh_url,
            json={"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"]},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert "access_token" in body
        assert "refresh_token" in body
        assert body["token_type"] == "bearer"

    async def test_refresh_token_missing_refresh_token(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
    ):
        # Act: omit the refresh_token field
        url = fastapi_app.url_path_for("refresh_token_route")
        response = await client.post(url, json={"access_token": "dummy"})

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_refresh_token_invalid_token(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
    ):
        # Act: provide a malformed refresh token
        url = fastapi_app.url_path_for("refresh_token_route")
        response = await client.post(
            url,
            json={"access_token": "dummy", "refresh_token": "invalid_token"},
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect token" in response.json()["detail"]
    
    async def test_refresh_token_blacklisted(
        self,
        client: AsyncClient,
        test_user: UserCreateDTO,
        fastapi_app: FastAPI,
        monkeypatch,
    ):
        # Arrange: create & confirm a user, then log in to get a real refresh token
        monkeypatch.setattr(UserModel, "generate_confirmation_token", lambda: "123456")
        user_data = test_user.model_dump()
        create_url = fastapi_app.url_path_for("create_user_route")
        await client.post(create_url, json=user_data)
        confirm_url = fastapi_app.url_path_for("confirm_email_route")
        await client.post(confirm_url, params={"confirmation_token": 123456})
        login_url = fastapi_app.url_path_for("login_route")
        login_resp = await client.post(
            login_url,
            data={"username": test_user.email, "password": test_user.password},
        )
        tokens = login_resp.json()

        # Simulate that the refresh token has been blacklisted
        from BMC_API.src.infrastructure.external_services.redis.token_cache_impl import (
            RedisTokenCache,
        )
        async def fake_get_token(self, token: str) -> bool:
            return True

        monkeypatch.setattr(
            RedisTokenCache,
            "get_token",
            fake_get_token,
        )

        # Act: attempt to refresh with the blacklisted token
        refresh_url = fastapi_app.url_path_for("refresh_token_route")
        response = await client.post(
            refresh_url,
            json={"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"]},
        )

        # Assert: should be rejected as invalid due to blacklist
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid refresh token" in response.json()["detail"]

