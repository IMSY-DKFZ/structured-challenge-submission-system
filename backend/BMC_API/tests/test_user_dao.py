# backend/BMC_API/tests/test_user_dao.py

import uuid
from datetime import datetime, timedelta

import pytest

from BMC_API.src.core.exceptions import RepositoryException
from BMC_API.src.domain.entities.user_model import UserModel
from BMC_API.src.infrastructure.persistence.dao.user_dao import SQLAlchemyUserRepository

pytest_plugins = [
    "BMC_API.tests.fixtures.user_fixtures",
]


@pytest.mark.anyio
class TestUserDAO:
    async def test_get_by_email(self, dbsession, test_user):
        # Arrange
        repo = SQLAlchemyUserRepository(dbsession)
        user_data = test_user.model_dump()
        new_user = UserModel.create_new(**user_data)
        await repo.create_obj(new_user)

        # Act
        found_user = await repo.get_by_email(test_user.email)

        # Assert
        assert found_user is not None
        assert found_user.email == test_user.email
        assert found_user.first_name == test_user.first_name
        assert found_user.last_name == test_user.last_name

    async def test_get_by_email_non_existent(self, dbsession):
        # Arrange
        repo = SQLAlchemyUserRepository(dbsession)

        # Act
        user = await repo.get_by_email("nonexistent@example.com")

        # Assert
        assert user is None

    async def test_update(self, dbsession, test_user):
        # Arrange
        repo = SQLAlchemyUserRepository(dbsession)
        user_data = test_user.model_dump()
        new_user = UserModel.create_new(**user_data)
        created_user = await repo.create_obj(new_user)

        from BMC_API.src.application.dto.user_dto import UserUpdateDTO

        update_data = UserUpdateDTO(first_name="Updated", last_name="Name")

        # Act
        updated_user = await repo.update(created_user.id, update_data.model_dump())

        # Assert
        assert updated_user.id == created_user.id
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"
        assert updated_user.email == test_user.email  # Unchanged

    #
    # async def test_update_non_existent_user(self, dbsession):
    #     # Arrange
    #     repo = SQLAlchemyUserRepository(dbsession)
    #     from BMC_API.src.application.dto.user_dto import UserUpdateDTO

    #     update_data = UserUpdateDTO(first_name="Updated")

    #     # Act & Assert
    #     with pytest.raises(UserNotFoundException):
    #         await repo.update(9999, update_data)

    async def test_confirm_email(self, dbsession, test_user):
        # Arrange
        repo = SQLAlchemyUserRepository(dbsession)
        user_data = test_user.model_dump()
        new_user = UserModel.create_new(**user_data)
        confirmation_token = "123456"
        new_user.email_confirmation_token = confirmation_token
        new_user.email_confirmed = False
        await repo.create_obj(new_user)

        # Act
        await repo.confirm_email(confirmation_token)
        updated_user = await repo.get_by_email(test_user.email)

        # Assert
        assert updated_user.email_confirmed is True
        assert updated_user.email_confirmation_token is None

    async def test_confirm_email_invalid_token(self, dbsession):
        # Arrange
        repo = SQLAlchemyUserRepository(dbsession)

        # Act & Assert
        with pytest.raises(RepositoryException, match="Invalid confirmation token"):
            await repo.confirm_email("invalid_token")

    async def test_confirm_email_already_confirmed(self, dbsession, test_user):
        # Arrange
        repo = SQLAlchemyUserRepository(dbsession)
        user_data = test_user.model_dump()
        new_user = UserModel.create_new(**user_data)
        confirmation_token = "123456"
        new_user.email_confirmation_token = confirmation_token
        new_user.email_confirmed = True  # Already confirmed
        await repo.create_obj(new_user)

        # Act & Assert
        with pytest.raises(RepositoryException, match="Email already confirmed"):
            await repo.confirm_email(confirmation_token)

    async def test_reset_password(self, dbsession, test_user):
        # Arrange
        repo = SQLAlchemyUserRepository(dbsession)
        user_data = test_user.model_dump()
        new_user = UserModel.create_new(**user_data)
        reset_token = str(uuid.uuid4())
        new_user.reset_token = reset_token
        await repo.create_obj(new_user)

        new_hashed_password = "new_hashed_password"

        # Act
        await repo.reset_password(reset_token, new_hashed_password)
        updated_user = await repo.get_by_email(test_user.email)

        # Assert
        assert updated_user.password == new_hashed_password
        assert updated_user.reset_token is None

    async def test_reset_password_invalid_token(self, dbsession):
        # Arrange
        repo = SQLAlchemyUserRepository(dbsession)

        # Act & Assert
        with pytest.raises(RepositoryException, match="Invalid reset token"):
            await repo.reset_password("invalid_token", "new_password")

    async def test_login(self, dbsession, test_user):
        # Arrange
        repo = SQLAlchemyUserRepository(dbsession)
        user_data = test_user.model_dump()
        new_user = UserModel.create_new(**user_data)
        await repo.create_obj(new_user)

        # Act
        await repo.login(test_user.email)
        updated_user = await repo.get_by_email(test_user.email)

        # Assert
        assert updated_user.last_login_time is not None
        # Check if the last_login_time is within the last minute
        assert (datetime.now() - updated_user.last_login_time) < timedelta(minutes=1)

    async def test_login_non_existent_user(self, dbsession):
        # Arrange
        repo = SQLAlchemyUserRepository(dbsession)

        # Act
        result = await repo.login("nonexistent@example.com")

        # Assert
        assert result is None
