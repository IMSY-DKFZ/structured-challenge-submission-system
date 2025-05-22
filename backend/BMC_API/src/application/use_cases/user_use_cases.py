# application/use_cases/user_use_cases.py
import uuid
from datetime import datetime, timedelta
from typing import Optional, Type

from fastapi import BackgroundTasks

# from fastapi import BackgroundTasks
from loguru import logger
from pydantic import BaseModel, ValidationError

from BMC_API.src.application.dto.user_dto import (
    Token,
    TokenData,
    UserCreateDTO,
    UserPasswordDTO,
    UserResponseDTO,
    UserUpdateDTO,
)
from BMC_API.src.application.interfaces.authentication import auth
from BMC_API.src.application.interfaces.email_scheduler import EmailSchedulerService
from BMC_API.src.application.interfaces.password_hasher_impl import BcryptPasswordHasher
from BMC_API.src.application.use_cases.base_use_cases import BaseService
from BMC_API.src.core.config.settings import settings
from BMC_API.src.core.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    RepositoryException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from BMC_API.src.domain.entities.user_model import UserModel
from BMC_API.src.domain.interfaces.token_cache import TokenCache
from BMC_API.src.domain.repositories.user_repository import UserRepositoryProtocol


class UserService(BaseService[UserModel, UserResponseDTO]):
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
        user_create: UserCreateDTO,
        background_tasks: BackgroundTasks,
    ) -> UserResponseDTO:
        # Check if user already exists.
        existing = await self.repository.get_by_email(user_create.email)
        if existing:
            raise UserAlreadyExistsException(email=user_create.email)

        # Check the password.
        try:
            UserPasswordDTO(password=user_create.password)
        except ValidationError as e:
            logger.error(e)
            raise RepositoryException(message=str(e.errors()[0]["msg"]))

        # Hash the password.
        hashed = self.password_hasher.hash(user_create.password)
        # user_data = user_create.copy(update={"password": hashed})

        # created: UserModel = await self.repository.create(user_data)

        user_data = user_create.model_dump()
        user_data["password"] = hashed
        new_user = UserModel.create_new(**user_data)

        # Persist the user (the repository no longer needs to set domain defaults)
        created: UserModel = await self.repository.create_obj(new_user)

        # Email code here
        if settings.environment == "dev":
            logger.debug(f"Email confirmation token for user {created.id}: {created.email_confirmation_token}")
        else:
            ### Send email_confirmation_token to User
            email_scheduler = EmailSchedulerService(background_tasks)
            email_scheduler.schedule_email_confirmation(user=created)

        try:
            return UserResponseDTO.model_validate(created)
        except ValidationError as e:
            logger.error(f"Failed to validate user response: {e}")
            raise RepositoryException(message="Error creating user response")
        except Exception as e:
            logger.error(e)
            raise RepositoryException(message="Error creating user response")

    async def update_user(
        self,
        id: int,
        user_update: UserUpdateDTO,
        active_user_password: str | None = None,
    ) -> UserResponseDTO:
        if id is None:
            raise ValueError("User id must be provided for update.")
        if hasattr(user_update, "password") and user_update.password is not None and active_user_password is None:
            raise RepositoryException(message="Existing password must be provided for updating password.")

        existing = await self.repository.get(id=id)
        if not existing:
            raise UserNotFoundException(id)

        if hasattr(user_update, "password") and user_update.password is not None:
            if not self.password_hasher.verify(active_user_password, existing.password):
                raise InvalidCredentialsException("Current password does not match.")

            try:
                UserPasswordDTO(password=user_update.password)
                hashed_password = self.password_hasher.hash(user_update.password)
                user_update.password = hashed_password
            except ValidationError as e:
                logger.error(e)
                raise RepositoryException(message=str(e.errors()[0]["msg"]))

        # Convert DTO to entity data
        entity_data = user_update.model_dump()
        entity_data["modified_time"] = datetime.now()

        return await super().update(id=id, model_update=entity_data)

    async def login_user(self, email: str, password: str) -> Token:
        """
        Logs in the user if a correct email & password combination is provided.
        Returns both access and refresh tokens.
        """

        email = email.lower()
        user = await self.repository.get_by_email(email)
        if not user:
            raise InvalidCredentialsException

        await auth.authenticate_user(email, password, self.repository)

        await self.repository.login(email)
        bearer_tokens: Token = auth.generate_bearer_tokens(TokenData(email=email))

        return bearer_tokens

    async def refresh_token(self, user_service_admin, token_data: Token, token_cache: TokenCache = None) -> Token:

        # 1. Check if there is a refresh_token
        refresh_token = token_data.refresh_token
        if not refresh_token:
            raise InvalidTokenException

        # 2. Decode and validate type of refresh_token
        refresh_token_payload = auth.decode_token(token_data.refresh_token)
        refresh_token_type = refresh_token_payload.get("type")
        email = refresh_token_payload.get("sub")
        
        if refresh_token_type is not None and refresh_token_type != "refresh":
            raise InvalidTokenException(message="Invalid refresh token")

        # 3. Check if refresh_token is stored Redis database before
        cache = token_cache if token_cache is not None else self.token_cache
        is_refresh_token_blacklisted = await cache.get_token(refresh_token)
        if is_refresh_token_blacklisted:
            """
            If someone is trying to use blacklisted token, this can mean that the token is stolen. In this case user is disabled. Admin is notified about the situation
            """
            if email is not None:
                user, *_ = await user_service_admin.list(search_filters={"email":email})
                user_id = user[0].id
                await user_service_admin.update(id=user_id, user_update={"disabled": True})
                
                #TODO: Send admin an e-mail about this
                logger.warning(
                    f"User [{email}] disabled because of usage of blacklisted token [{refresh_token}]!"
                )

            raise InvalidTokenException(message="Invalid refresh token") # Just send general error, don't give detail.
        
        # 4. If to issue found, continue token refreshing procedure
        bearer_tokens: Token = auth.generate_bearer_tokens(TokenData(email=email))
        return bearer_tokens
        
    async def logout_user(self, token_data: Token, token_cache: TokenCache = None) -> None:
        access_token_payload = auth.decode_token(token_data.access_token)
        access_token_type = access_token_payload.get("type", None)

        if access_token_type is not None and access_token_type != "access":
            raise InvalidTokenException(message="Invalid access token")

        refresh_token_payload = auth.decode_token(token_data.refresh_token)
        refresh_token_type = refresh_token_payload.get("type")

        if refresh_token_type is not None and refresh_token_type != "refresh":
            raise InvalidTokenException(message="Invalid refresh token")

        cache = token_cache if token_cache is not None else self.token_cache
        try:
            await cache.set_token(
                key=token_data.access_token,
                value=str(datetime.now()),
                expire=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            )
            await cache.set_token(
                key=token_data.refresh_token,
                value=str(datetime.now()),
                expire=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            )
        except Exception as e:
            raise RepositoryException("Error setting token in cache") from e

    async def confirm_email(self, confirmation_token: str) -> None:
        await self.repository.confirm_email(confirmation_token)

    async def reset_password_request(self, email: str, background_tasks: BackgroundTasks) -> None:
        user = await self.repository.get_by_email(email)
        if not user:
            raise UserNotFoundException(message=f"User with email {email} not found.")
        if not user.email_confirmed:
            raise RepositoryException(message="Email not confirmed. Please verify your email address.")
        if user.disabled:
            raise RepositoryException(message="User account disabled. Please contact Technical Support.")

        # Generate reset token
        reset_token: str = str(uuid.uuid4())
        user.reset_token = reset_token
        await self.repository.update_obj(user)

        if settings.environment == "dev":
            logger.debug(f"Reset password token for user {user.id}: {user.reset_token}")
        else:
            ### Send reset_token to User
            email_scheduler = EmailSchedulerService(background_tasks)
            email_scheduler.schedule_email_reset_password(user=user)

    async def reset_password(self, reset_token: str, new_password: str) -> None:
        # Validate password first
        try:
            UserPasswordDTO(password=new_password)
        except ValidationError as e:
            logger.error(e)
            raise RepositoryException(message=str(e.errors()[0]["msg"]))
        except Exception as e:
            logger.error(e)
            raise RepositoryException(message="Error creating user response")

        hashed = self.password_hasher.hash(new_password)
        await self.repository.reset_password(reset_token, hashed)
