# backend/BMC_API/src/application/interfaces/authentication.py
from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import EmailStr

from BMC_API.src.api.dependencies.route_dependencies import get_repository
from BMC_API.src.api.schemas.user_schema import UserInDB
from BMC_API.src.application.dto.user_dto import Token, TokenData
from BMC_API.src.application.interfaces.password_hasher_impl import BcryptPasswordHasher
from BMC_API.src.core.config.settings import settings
from BMC_API.src.core.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    RepositoryException,
    UserNotAuthenticatedException,
    UserNotFoundException,
)
from BMC_API.src.domain.entities.user_model import UserModel
from BMC_API.src.infrastructure.persistence.dao.user_dao import SQLAlchemyUserRepository

# Global settings and prefix (they will be “copied” into the class attributes)
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS
API_PREFIX = settings.api_prefix
auth_header = {"WWW-Authenticate": "Bearer"}


class Auth:
    # Class-level configuration variables
    SECRET_KEY = SECRET_KEY
    ALGORITHM = ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_DAYS = REFRESH_TOKEN_EXPIRE_DAYS
    auth_header = auth_header
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/user/token", auto_error=False)
    password_hasher = BcryptPasswordHasher()
    # @staticmethod
    # def verify_password(plain_password: str, hashed_password: str) -> bool:
    #     """
    #     Compare a plain text password with its bcrypt hash.
    #     """
    #     # Ensure both values are bytes.
    #     if not isinstance(plain_password, bytes):
    #         plain_password = plain_password.encode("utf-8")
    #     if not isinstance(hashed_password, bytes):
    #         hashed_password = hashed_password.encode("utf-8")
    #     return bcrypt.checkpw(plain_password, hashed_password)

    # @staticmethod
    # def get_password_hash(password: str) -> str:
    #     """
    #     Generate a bcrypt hash of the given password.
    #     """
    #     return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10)).decode(
    #         "utf-8"
    #     )

    async def get_user(self, email: str, repository: SQLAlchemyUserRepository) -> UserModel:
        """
        Retrieve a user from the database by email.
        Also checks if the user has confirmed the email and is not disabled.
        """
        user: UserModel = await repository.get_by_email(email=email)
        if not user:
            raise UserNotFoundException(message="Incorrect email or password")
        if not user.email_confirmed:
            raise RepositoryException(message="Email not confirmed. Please verify your email address.")
        if user.disabled:
            raise RepositoryException(message="User account disabled. Please contact Technical Support.")
        return user

    async def authenticate_user(
        self, email: EmailStr, password: str, repository: SQLAlchemyUserRepository
    ) -> Optional[UserModel]:
        """
        Validate the user's credentials. Returns the user if valid;
        otherwise returns False.
        """
        try:
            user: UserModel = await self.get_user(email, repository)
        except:
            raise

        # if not user:
        #     return False
        if not self.password_hasher.verify(password, user.password):
            raise InvalidCredentialsException
        return user

    def create_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """
        Create a JWT with an expiration time. The extracted token type
        (e.g. "access" or "refresh") from data.type is added to the payload.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=15)
        to_encode.update({"exp": expire, "type": data.get("type")})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def generate_bearer_tokens(self, token_data: TokenData) -> Token:
        access_token = self.create_token(
            data={"sub": token_data.email, "type": "access"},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = self.create_token(
            data={"sub": token_data.email, "type": "refresh"},
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        bearer_tokens = Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
        return bearer_tokens

    def decode_token(self, token: str) -> dict:
        """
        Decode a JWT token and return its payload.
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except JWTError:
            raise InvalidTokenException

    async def validate_current_access_token(self, access_token: str) -> Optional[str]:
        """
        Validates the current access token by checking its expiration,
        token type and required payload (such as the subject).
        """
        if not access_token:
            return None
        payload = self.decode_token(access_token)
        email = payload.get("sub")
        exp = payload.get("exp")
        token_type = payload.get("type")
        if token_type != "access":
            raise InvalidCredentialsException
        if email is None or exp is None:
            raise InvalidCredentialsException
        if datetime.now() >= datetime.fromtimestamp(exp):
            raise InvalidTokenException(message="Authentication credentials expired.")
        return access_token

    # async def validate_active_user_password(
    #     self, current_user: UserModel, active_user_password: str
    # ) -> UserModel:
    #     """
    #     Validates the current user's password for sensitive operations.
    #     This is used when additional confirmation is required for critical actions.

    #     Args:
    #         current_user: The authenticated user model
    #         active_user_password: The password provided for confirmation

    #     Returns:
    #         The current user if validation is successful

    #     Raises:
    #         InvalidCredentialsException: If the password is invalid or missing
    #     """
    #     if not active_user_password:
    #         raise InvalidCredentialsException(
    #             message="Password confirmation is required"
    #         )
    #     user: UserModel = await self.get_user(current_user.email, repository)

    #     if not self.password_hasher.verify(active_user_password, user.password):
    #         raise InvalidCredentialsException(message="Invalid password confirmation")

    #     return current_user

    async def get_current_user(self, access_token: str, repository: SQLAlchemyUserRepository) -> UserModel:
        """
        Retrieve the current user based on the provided access token.
        """

        if not access_token:
            return None

        try:
            payload = jwt.decode(access_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email: Optional[str] = payload.get("sub")
            if email is None:
                raise InvalidCredentialsException
            token_data = TokenData(email=email)
        except JWTError:
            raise InvalidTokenException

        user: UserModel = await self.get_user(token_data.email, repository)
        if user is None:
            raise InvalidCredentialsException
        return user

    async def get_current_active_user(self, current_user: UserModel = None) -> UserModel:
        """
        Verifies that the current user is active.
        """
        if not current_user:
            raise UserNotAuthenticatedException(message="User not authenticated")
        if current_user and current_user.disabled:
            raise RepositoryException(message="Inactive user")
        return current_user


# ---------------------
# Dependency wrappers
# ----------------------
# Create a single instance of Auth to use in the dependency functions.
auth = Auth()


# Dependency wrappers that called from router functions returns Pydantic models,
# because it is expected from FastAPI's dependency injection method.,


async def validate_current_access_token_dependency(
    access_token: Annotated[str, Depends(Auth.oauth2_scheme)],
) -> str:
    """
    FastAPI dependency that validates the current access token.
    """
    return await auth.validate_current_access_token(access_token)


async def get_current_user_dependency(
    access_token: Annotated[str, Depends(validate_current_access_token_dependency)],
    repository: Annotated[SQLAlchemyUserRepository, Depends(get_repository(SQLAlchemyUserRepository))],
) -> UserInDB:
    current_user: UserModel = await auth.get_current_user(access_token, repository)
    if not current_user:
        return None
    return UserInDB.from_orm(current_user)


async def get_current_active_user_dependency(
    current_user: Annotated[UserInDB, Depends(get_current_user_dependency)] = None,
) -> UserInDB:
    """
    FastAPI dependency that returns the current active user.
    """
    current_active_user: UserModel = await auth.get_current_active_user(current_user)
    return UserInDB.from_orm(current_active_user)


async def ensure_current_active_user(
    current_active_user: Annotated[Optional[UserInDB], Depends(get_current_active_user_dependency)] = None,
) -> Optional[UserInDB]:
    if not current_active_user:
        raise UserNotAuthenticatedException
    return current_active_user


async def validate_active_user_password_dependency(
    current_user: Annotated[UserInDB, Depends(get_current_active_user_dependency)],
    repository: Annotated[SQLAlchemyUserRepository, Depends(get_repository(SQLAlchemyUserRepository))],
    active_user_password: Annotated[
        str,
        Query(
            embed=True,
            description="Password confirmation for sensitive operations",
            examples=["your_secure_password"],
        ),
    ],
) -> UserInDB:
    """
    FastAPI dependency that validates the current user's password.
    This is used for sensitive operations that require password confirmation.
    """

    await auth.authenticate_user(email=current_user.email, password=active_user_password, repository=repository)
    return current_user
