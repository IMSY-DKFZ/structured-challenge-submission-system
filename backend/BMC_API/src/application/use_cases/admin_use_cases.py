# application/use_cases/admin_use_cases.py

from typing import Any, Dict, List, Optional, Type

from fastapi import BackgroundTasks

# from fastapi import BackgroundTasks
from loguru import logger
from pydantic import BaseModel, ValidationError

from BMC_API.src.api.dependencies.schemas import BulkOperationResponse
from BMC_API.src.application.dto.user_dto import (
    UserCreateAdminDTO,
    UserPasswordDTO,
    UserResponseAdminDTO,
    UserUpdateAdminDTO,
)
from BMC_API.src.application.interfaces.email_scheduler import EmailSchedulerService
from BMC_API.src.application.interfaces.password_hasher_impl import BcryptPasswordHasher
from BMC_API.src.application.use_cases.base_use_cases import BaseService
from BMC_API.src.core.config.settings import settings
from BMC_API.src.core.exceptions import RepositoryException, UserAlreadyExistsException
from BMC_API.src.domain.entities.user_model import UserModel
from BMC_API.src.domain.interfaces.token_cache import TokenCache
from BMC_API.src.domain.repositories.user_repository import UserRepositoryProtocol


class AdminUserService(BaseService[UserModel, UserResponseAdminDTO]):
    def __init__(
        self,
        repository: UserRepositoryProtocol,
        dto_class: Optional[Type[BaseModel]] = None,
        token_cache: Optional[TokenCache] = None,
    ) -> None:
        super().__init__(repository, dto_class)
        self.token_cache = token_cache
        self.password_hasher = BcryptPasswordHasher()

    async def create_user(
        self,
        background_tasks: BackgroundTasks,
        user_create: UserCreateAdminDTO,
    ) -> UserResponseAdminDTO:
        """
        Create a new user with password hashing and email confirmation.
        This method extends the base create method with user-specific functionality.
        """

        # Check if user already exists.
        existing = await self.repository.get_by_email(user_create.email)
        if existing:
            raise UserAlreadyExistsException(email=user_create.email)

        # Hash the password.
        hashed = self.password_hasher.hash(user_create.password)

        # Create a modified DTO with the hashed password
        user_data = user_create.model_dump()
        user_data["password"] = hashed

        # Use the entity class to create a new user model
        new_user = UserModel.create_new(**user_data)

        try:
            # Persist the user (the repository no longer needs to set domain defaults)
            created: UserModel = await self.repository.create_obj(new_user)

            # Send email confirmation
            if settings.environment == "dev":
                logger.debug(f"Email confirmation token for user {created.id}: {created.email_confirmation_token}")
            else:
                # Send email_confirmation_token to User
                email_scheduler = EmailSchedulerService(background_tasks)
                email_scheduler.schedule_email_confirmation(user=created)

            return UserResponseAdminDTO.model_validate(created)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise RepositoryException(message=f"Error creating user: {str(e)}")

    async def update(
        self,
        id: int,
        user_update: Dict,
    ) -> UserResponseAdminDTO:
        if id is None:
            raise ValueError("id must be provided for update.")

        if "password" in user_update and user_update["password"] is not None:
            try:
                UserPasswordDTO(password=user_update["password"])
                hashed_password = self.password_hasher.hash(user_update["password"])
                user_update["password"] = hashed_password
            except ValidationError as e:
                logger.error(e)
                raise RepositoryException(message=str(e.errors()[0]["msg"]))
        return await super().update(id=id, model_update=user_update)

    async def update_bulk(self, updates: List[Dict[str, Any]]) -> BulkOperationResponse[UserResponseAdminDTO]:
        # Call the parent's update_bulk with your specific DTO class
        # This replaces the generic UpdateDTO with your specific UserUpdateAdminDTO
        return await super().update_bulk(updates, update_dto_class=UserUpdateAdminDTO)


# class AdminConferenceService(BaseService[ConferenceModel, ConferenceResponseAdminDTO]):
#     def __init__(
#         self,
#         repository: ConferenceRepositoryProtocol,
#         dto_class: Optional[Type[BaseModel]] = None,
#     ) -> None:
#         super().__init__(repository, ConferenceResponseAdminDTO)

#     async def list_conferences_of_user(
#         self, user_id: int, offset: int = 0, limit: int = 50
#     ) -> Optional[ConferenceResponseAdminDTO]:
#         search_filters = {"owner_id": user_id}
#         return await super().list(offset=offset, limit=limit, search_filters=search_filters)
