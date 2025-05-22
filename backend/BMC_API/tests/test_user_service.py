# backend/BMC_API/tests/unit/test_user_service.py
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from BMC_API.src.application.dto.user_dto import Token, UserResponseDTO, UserUpdateDTO
from BMC_API.src.application.interfaces.authentication import auth
from BMC_API.src.application.use_cases.user_use_cases import UserService
from BMC_API.src.core.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    RepositoryException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from BMC_API.src.domain.entities.user_model import UserModel

pytest_plugins = [
    "BMC_API.tests.fixtures.user_fixtures",
]

@pytest.mark.anyio
class TestUserService:
    
    async def test_create_user_success(self, test_user):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.get_by_email.return_value = None  # User doesn't exist yet

        # Mock the password_hasher to avoid the encoding issue
        mock_password_hasher = MagicMock()
        mock_password_hasher.hash.return_value = "hashed_password"

        # Create a user model with the expected fields after creation
        user_model = MagicMock(spec=UserModel)
        user_model.id = 1
        user_model.email = test_user.email
        user_model.first_name = test_user.first_name
        user_model.last_name = test_user.last_name
        user_model.email_confirmation_token = "confirmation_token"
        user_model.bio = ""
        user_model.city = ""
        user_model.country = ""
        user_model.institution = ""
        user_model.titel = ""
        user_model.website = ""
        user_model.notifications = json.dumps({})

        # Mock the repository create_obj to return our mocked user model
        mock_repository.create_obj.return_value = user_model

        # Mock the background tasks
        mock_background_tasks = MagicMock()

        # Create service with mocked repository and password hasher
        service = UserService(repository=mock_repository)
        service.password_hasher = mock_password_hasher  # Replace the password hasher with our mock

        # Mock UserModel.create_new to avoid the actual call
        with patch(
            "BMC_API.src.domain.entities.user_model.UserModel.create_new",
            return_value=user_model,
        ):
            # Act - Note that the correct parameter order is background_tasks first, then user_create
            result = await service.create_user(background_tasks=mock_background_tasks, user_create=test_user)

        # Assert
        mock_repository.get_by_email.assert_called_once_with(test_user.email)
        mock_repository.create_obj.assert_called_once()
        mock_password_hasher.hash.assert_called_once_with(test_user.password)
        assert isinstance(result, UserResponseDTO)
        assert result.email == test_user.email
        assert result.first_name == test_user.first_name
        assert result.last_name == test_user.last_name

    
    async def test_create_user_already_exists(self, test_user):
        # Arrange
        mock_repository = AsyncMock()

        # Mock that the user already exists in the database
        existing_user = MagicMock(spec=UserModel)
        existing_user.email = test_user.email
        mock_repository.get_by_email.return_value = existing_user

        mock_background_tasks = MagicMock()

        service = UserService(repository=mock_repository)

        # Act & Assert
        with pytest.raises(UserAlreadyExistsException) as excinfo:
            await service.create_user(background_tasks=mock_background_tasks, user_create=test_user)

        # Verify exception details
        assert test_user.email in str(excinfo.value)

        # Verify repository interactions
        mock_repository.get_by_email.assert_called_once_with(test_user.email)
        # Ensure create_obj was never called since user already exists
        mock_repository.create_obj.assert_not_called()

    
    async def test_update_user_success(self, test_user):
        # Arrange
        mock_repository = AsyncMock()
        user_model = UserModel.create_new(**test_user.model_dump())
        user_model.id = 1
        mock_repository.get.return_value = user_model

        updated_model = UserModel.create_new(**test_user.model_dump())
        updated_model.id = 1
        updated_model.first_name = "Updated"
        mock_repository.update.return_value = updated_model

        update_dto = UserUpdateDTO(first_name="Updated")

        service = UserService(repository=mock_repository)

        # Act
        result = await service.update_user(1, update_dto)

        # Assert: Expecting repository.get to be called twice with id=1.
        mock_repository.get.assert_called_with(id=1)
        assert mock_repository.get.call_count == 2

        assert result.first_name == "Updated"

    
    async def test_update_user_not_found(self):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.get.return_value = None

        update_dto = UserUpdateDTO(first_name="Updated")

        service = UserService(repository=mock_repository)

        # Act & Assert
        with pytest.raises(UserNotFoundException):
            await service.update_user(999, update_dto)

        mock_repository.get.assert_called_once_with(id=999)
        mock_repository.update.assert_not_called()

    
    async def test_update_user_change_password_success(self, test_user):
        # Arrange
        mock_repository = AsyncMock()
        user_model = UserModel.create_new(**test_user.model_dump())
        user_model.id = 1
        user_model.password = "$2b$10$soMeHashEdPaSsWoRd"
        mock_repository.get.return_value = user_model

        updated_model = UserModel.create_new(**test_user.model_dump())
        updated_model.id = 1
        updated_model.password = "$2b$10$neWHashEdPaSsWoRd"
        mock_repository.update.return_value = updated_model

        update_dto = UserUpdateDTO(password="NewPassword94215!")

        service = UserService(repository=mock_repository)
        service.password_hasher.verify = MagicMock(return_value=True)
        service.password_hasher.hash = MagicMock(return_value="$2b$10$neWHashEdPaSsWoRd")

        # Act
        result = await service.update_user(1, update_dto, active_user_password="CurrentPassword94215!")

        # Assert: Expecting repository.get to be called twice with id=1.
        mock_repository.get.assert_called_with(id=1)
        assert mock_repository.get.call_count == 2

        service.password_hasher.verify.assert_called_once_with("CurrentPassword94215!", "$2b$10$soMeHashEdPaSsWoRd")
        service.password_hasher.hash.assert_called_once_with("NewPassword94215!")
        mock_repository.update.assert_called_once()

    
    async def test_update_user_change_password_wrong_current_password(self, test_user):
        # Arrange
        mock_repository = AsyncMock()
        user_model = UserModel.create_new(**test_user.model_dump())
        user_model.id = 1
        user_model.password = "$2b$10$soMeHashEdPaSsWoRd"  # Mocked hashed password
        mock_repository.get.return_value = user_model

        # Create update DTO with new password
        update_dto = UserUpdateDTO(password="NewPassword94215!")

        # Mock password verification to fail
        service = UserService(repository=mock_repository)
        service.password_hasher.verify = MagicMock(return_value=False)

        # Act & Assert
        with pytest.raises(InvalidCredentialsException, match="Current password does not match"):
            await service.update_user(1, update_dto, active_user_password="WrongPassword94215!")

        mock_repository.get.assert_called_once_with(id=1)
        service.password_hasher.verify.assert_called_once_with("WrongPassword94215!", "$2b$10$soMeHashEdPaSsWoRd")
        mock_repository.update.assert_not_called()

    
    async def test_login_user_success(self, test_user):
        # Arrange
        mock_repository = AsyncMock()
        user_model = UserModel.create_new(**test_user.model_dump())
        mock_repository.get_by_email.return_value = user_model

        # Mock auth.authenticate_user
        with patch(
            "BMC_API.src.application.interfaces.authentication.auth.authenticate_user",
            new_callable=AsyncMock,
        ) as mock_auth:
            mock_auth.return_value = user_model

            # Mock auth.generate_bearer_tokens
            with patch("BMC_API.src.application.interfaces.authentication.auth.generate_bearer_tokens") as mock_token:
                expected_token = Token(
                    access_token="mock_access_token",
                    refresh_token="mock_refresh_token",
                    token_type="bearer",
                )
                mock_token.return_value = expected_token

                service = UserService(repository=mock_repository)

                # Act
                result = await service.login_user(test_user.email, test_user.password)

                # Assert
                mock_repository.get_by_email.assert_called_once_with(test_user.email.lower())
                mock_auth.assert_called_once_with(test_user.email.lower(), test_user.password, mock_repository)
                mock_repository.login.assert_called_once_with(test_user.email.lower())
                assert result == expected_token

    
    async def test_login_user_not_found(self, test_user):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.get_by_email.return_value = None  # User not found

        service = UserService(repository=mock_repository)

        # Act & Assert
        with pytest.raises(InvalidCredentialsException):
            await service.login_user(test_user.email, test_user.password)

        mock_repository.get_by_email.assert_called_once_with(test_user.email.lower())

    
    async def test_logout_user_success(self):
        # Arrange
        mock_repository = AsyncMock()
        mock_token_cache = AsyncMock()

        token_data = Token(
            access_token="mock_access_token",
            refresh_token="mock_refresh_token",
            token_type="bearer",
        )

        # Mock auth.decode_token for access token
        with patch("BMC_API.src.application.interfaces.authentication.auth.decode_token") as mock_decode_access:
            mock_decode_access.side_effect = [
                {"type": "access"},  # For access token
                {"type": "refresh"},  # For refresh token
            ]

            service = UserService(repository=mock_repository, token_cache=mock_token_cache)

            # Act
            await service.logout_user(token_data, mock_token_cache)

            # Assert
            mock_decode_access.assert_any_call("mock_access_token")
            mock_decode_access.assert_any_call("mock_refresh_token")
            assert mock_decode_access.call_count == 2

            # Check if token cache was called to set tokens
            assert mock_token_cache.set_token.call_count == 2

    
    async def test_confirm_email_success(self):
        # Arrange
        mock_repository = AsyncMock()
        confirmation_token = "123456"

        service = UserService(repository=mock_repository)

        # Act
        await service.confirm_email(confirmation_token)

        # Assert
        mock_repository.confirm_email.assert_called_once_with(confirmation_token)

    
    async def test_reset_password_request_success(self, test_user):
        # Arrange
        mock_repository = AsyncMock()
        user_model = UserModel.create_new(**test_user.model_dump())
        user_model.id = 1
        user_model.email_confirmed = True
        mock_repository.get_by_email.return_value = user_model

        mock_background_tasks = MagicMock()

        with patch("uuid.uuid4", return_value="mock-uuid"):
            service = UserService(repository=mock_repository)

            # Act
            await service.reset_password_request(test_user.email, mock_background_tasks)

            # Assert
            mock_repository.get_by_email.assert_called_once_with(test_user.email)
            mock_repository.update_obj.assert_called_once()
            # Check if user model's reset_token was updated
            assert user_model.reset_token == "mock-uuid"

    
    async def test_reset_password_request_user_not_found(self):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.get_by_email.return_value = None

        mock_background_tasks = MagicMock()

        service = UserService(repository=mock_repository)

        # Act & Assert
        with pytest.raises(UserNotFoundException):
            await service.reset_password_request("nonexistent@example.com", mock_background_tasks)

        mock_repository.get_by_email.assert_called_once_with("nonexistent@example.com")
        mock_repository.update_obj.assert_not_called()

    
    async def test_reset_password_success(self):
        # Arrange
        mock_repository = AsyncMock()
        reset_token = "mock-reset-token"
        new_password = "NewSecurePassword94215!"
        hashed_password = "$2b$10$neWHashEdPaSsWoRd"

        service = UserService(repository=mock_repository)
        service.password_hasher.hash = MagicMock(return_value=hashed_password)

        # Act
        await service.reset_password(reset_token, new_password)

        # Assert
        service.password_hasher.hash.assert_called_once_with(new_password)
        mock_repository.reset_password.assert_called_once_with(reset_token, hashed_password)

    
    async def test_reset_password_validation_error(self):
        # Arrange
        mock_repository = AsyncMock()
        reset_token = "mock-reset-token"
        invalid_password = "short"  # Too short to pass validation

        service = UserService(repository=mock_repository)

        # Act & Assert
        with pytest.raises(RepositoryException):
            await service.reset_password(reset_token, invalid_password)

        mock_repository.reset_password.assert_not_called()

    async def test_refresh_token_missing_refresh_token(self):
        mock_repo = AsyncMock()
        service = UserService(repository=mock_repo)
        admin_service = AsyncMock()
        token_data = Token(access_token="foo", refresh_token="")

        with pytest.raises(InvalidTokenException):
            await service.refresh_token(admin_service, token_data)

    async def test_refresh_token_invalid_type(self, monkeypatch):
        mock_repo = AsyncMock()
        service = UserService(repository=mock_repo)
        admin_service = AsyncMock()
        token_cache = AsyncMock()

        # decode_token returns wrong type
        monkeypatch.setattr(
            auth, "decode_token", lambda t: {"type": "access", "sub": "user@example.com"}
        )
        token_data = Token(access_token="foo", refresh_token="bar")

        with pytest.raises(InvalidTokenException) as exc:
            await service.refresh_token(admin_service, token_data, token_cache)
        assert "Invalid refresh token" in str(exc.value)

    async def test_refresh_token_blacklisted(self, monkeypatch):
        mock_repo = AsyncMock()
        service = UserService(repository=mock_repo)

        # stubbed admin service
        admin_service = AsyncMock()
        async def fake_list(search_filters):
            class U: id = 42
            return ([U()], None, None)
        admin_service.list.side_effect = fake_list
        admin_service.update = AsyncMock()

        # stubbed token cache that says token is blacklisted
        token_cache = AsyncMock()
        async def fake_get(token):
            return True
        token_cache.get_token.side_effect = fake_get

        # decode_token returns a valid refresh token payload
        monkeypatch.setattr(
            auth, "decode_token", lambda t: {"type": "refresh", "sub": "user@example.com"}
        )
        token_data = Token(access_token="foo", refresh_token="blacklisted")

        with pytest.raises(InvalidTokenException):
            await service.refresh_token(admin_service, token_data, token_cache)

        admin_service.update.assert_awaited_once_with(id=42, user_update={"disabled": True})


    async def test_refresh_token_success(self, monkeypatch):
        mock_repo = AsyncMock()
        service = UserService(repository=mock_repo)
        admin_service = AsyncMock()
        token_cache = AsyncMock()

        # decode_token returns a valid refresh payload
        monkeypatch.setattr(
            auth, "decode_token", lambda t: {"type": "refresh", "sub": "user@example.com"}
        )
        async def fake_get(token):
            return False
        token_cache.get_token.side_effect = fake_get

        # generate_bearer_tokens returns known tokens
        expected = Token(access_token="new_access", refresh_token="new_refresh")
        monkeypatch.setattr(
            auth, "generate_bearer_tokens", lambda data: expected
        )

        token_data = Token(access_token="foo", refresh_token="valid")
        result = await service.refresh_token(admin_service, token_data, token_cache)

        assert result == expected