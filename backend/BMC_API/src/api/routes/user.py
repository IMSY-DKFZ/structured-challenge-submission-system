# backend/BMC_API/src/api/routes/user.py
# Exceptions raised the routes here will be caught by the global exception handlers.

from typing import Annotated, Optional

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    HTTPException,
    Query,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from pydantic import EmailStr

from BMC_API.src.api.dependencies.route_dependencies import get_repository, get_service
from BMC_API.src.api.dependencies.schemas import PaginationResponse
from BMC_API.src.api.schemas.user_schema import UserInDB
from BMC_API.src.application.dto.challenge_dto import ChallengeModelBaseOutputDTO
from BMC_API.src.application.dto.task_dto import TaskModelBaseOutputDTO
from BMC_API.src.application.dto.user_dto import (
    Token,
    UserCreateDTO,
    UserResponseAdminDTO,
    UserResponseDTO,
    UserUpdateDTO,
)
from BMC_API.src.application.interfaces.authentication import (
    auth_header,
    ensure_current_active_user,
    get_current_user_dependency,
)
from BMC_API.src.application.use_cases.admin_use_cases import AdminUserService
from BMC_API.src.application.use_cases.challenge_use_cases import ChallengeService
from BMC_API.src.application.use_cases.task_use_cases import TaskService
from BMC_API.src.application.use_cases.user_use_cases import UserService
from BMC_API.src.core.exceptions import UserNotFoundException
from BMC_API.src.infrastructure.external_services.redis.dependency import (
    get_token_cache,
)
from BMC_API.src.infrastructure.external_services.redis.token_cache_impl import (
    RedisTokenCache,
)
from BMC_API.src.infrastructure.persistence.dao.challenge_dao import (
    SQLAlchemyChallengeRepository,
)
from BMC_API.src.infrastructure.persistence.dao.task_dao import SQLAlchemyTaskRepository
from BMC_API.src.infrastructure.persistence.dao.user_dao import SQLAlchemyUserRepository

router = APIRouter()


# Dependency functions
repository_dependency = get_repository(SQLAlchemyUserRepository)
service_dependency = get_service(UserService, repository_dependency, dto_class=UserResponseDTO)
service_dependency_admin = get_service(AdminUserService, repository_dependency, dto_class=UserResponseAdminDTO)

task_repository_dependency = get_repository(SQLAlchemyTaskRepository)
task_service_dependency = get_service(TaskService, task_repository_dependency, dto_class=TaskModelBaseOutputDTO)

challenge_repository_dependency = get_repository(SQLAlchemyChallengeRepository)
challenge_service_dependency = get_service(
    ChallengeService, challenge_repository_dependency, dto_class=ChallengeModelBaseOutputDTO
)


# Routes
@router.post("/create", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_user_route(
    user: Annotated[
        UserCreateDTO,
        Body(
            ...,
            description="User creation details, including email, password, and other required fields.",
        ),
    ],
    background_tasks: BackgroundTasks,
    service: Annotated[UserService, Depends(service_dependency)],
    current_user: Annotated[Optional[UserInDB], Depends(get_current_user_dependency)] = None,
) -> UserResponseDTO:
    """
    Create a new user. Prevents account creation if a user is already logged in.
    """
    logger.info("Received request to create user with email: {}", user.email)
    if current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cannot create new account while logged in.",
            headers=auth_header,
        )
    created_user: UserResponseDTO = await service.create_user(user_create=user, background_tasks=background_tasks)
    logger.info("User created successfully: {}", user.email)
    return created_user


@router.put("/update", response_model=UserResponseDTO)
async def update_user_route(
    updated_data: Annotated[
        UserUpdateDTO,
        Body(..., description="The updated user details (e.g., new email, name, etc.)."),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[UserService, Depends(service_dependency)],
    active_user_password: Annotated[Optional[str], Query(description="The current password for verification.")] = None,
) -> UserResponseDTO:
    """
    Update an existing user's details. The user ID is taken from the authenticated user.
    """
    id = current_active_user.id
    logger.info("Received request to update user with id: {}", id)
    updated_user: UserResponseDTO = await service.update_user(
        id=id,
        user_update=updated_data,
        active_user_password=active_user_password,
    )
    logger.info("User with id: {} updated successfully.", id)
    return updated_user


@router.post("/token", response_model=Token)
async def login_route(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[UserService, Depends(service_dependency)],
) -> Token:
    """
    Logs in the user if a correct email & password combination is provided.
    Returns both access and refresh tokens.
    """
    logger.info("Received login request for email: {}", form_data.username)
    bearer_tokens: Token = await service.login_user(email=form_data.username, password=form_data.password)
    logger.info("Login request for email {} successful.", form_data.username)
    return bearer_tokens


@router.post("/refresh_token", response_model=Token)
async def refresh_token_route(
    token_data: Annotated[
        Token,
        Body(
            ...,
            description="Token object containing the refresh token to be refreshed.",
        ),
    ],
    service: Annotated[UserService, Depends(service_dependency)],
    service_admin: Annotated[AdminUserService, Depends(service_dependency_admin)],
    token_cache: Annotated[RedisTokenCache, Depends(get_token_cache)],
) -> Token:
    """
    Generates and returns new access token.
    """
    """
    If refresh token is blacklisted, takes necessary security measurements at below.
    ------------------------------
    Refresh Token Automatic Reuse Detection (taken from --> https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/)

    Refresh tokens are bearer tokens. It's impossible for the authorization server to know who is legitimate or malicious when receiving a new access token request. We could then treat all users as potentially malicious.

    How could we handle a situation where there is a race condition between a legitimate user and a malicious one? For example:

    1) 🐱 Legitimate User has 🔄 Refresh Token 1 and 🔑 Access Token 1.
    2) 😈 Malicious User manages to steal 🔄 Refresh Token 1 from 🐱 Legitimate User.
    3) 🐱 Legitimate User uses 🔄 Refresh Token 1 to get a new refresh-access token pair.
    4) The 🚓 Auth0 Authorization Server returns 🔄 Refresh Token 2 and 🔑 Access Token 2 to 🐱 Legitimate User.
    5) 😈 Malicious User then attempts to use 🔄 Refresh Token 1 to get a new access token. Pure evil!


    What do you think should happen next? Would 😈 Malicious User manage to get a new access token?
    This is what happens when your identity platform has 🤖 Automatic Reuse Detection:

    1) The 🚓 Auth0 Authorization Server has been keeping track of all the refresh tokens descending from the original refresh token. That is, it has created a "token family".
    2) The 🚓 Auth0 Authorization Server recognizes that someone is reusing 🔄 Refresh Token 1 and immediately invalidates the refresh token family, including 🔄 Refresh Token 2.
    3) The 🚓 Auth0 Authorization Server returns an Access Denied response to 😈 Malicious User.
    4) 🔑 Access Token 2 expires, and 🐱 Legitimate User attempts to use 🔄 Refresh Token 2 to request a new refresh-access token pair.
    5) The 🚓 Auth0 Authorization Server returns an Access Denied response to 🐱 Legitimate User.
    6) The 🚓 Auth0 Authorization Server requires re-authentication to get new access and refresh tokens.
    """
    logger.info("Received new token request")
    bearer_tokens: Token = await service.refresh_token(user_service_admin=service_admin, token_data=token_data, token_cache=token_cache)
    logger.info("New tokens created successfully.")
    return bearer_tokens


@router.post("/logout")
async def logout_token_route(
    token_data: Annotated[
        Token,
        Body(
            ...,
            description="Token object representing the user's session token to be invalidated.",
        ),
    ],
    service: Annotated[UserService, Depends(service_dependency)],
    token_cache: Annotated[RedisTokenCache, Depends(get_token_cache)],
) -> dict:
    """
    Logs out the user by invalidating the provided token.
    """
    logger.info("Received logout request")
    await service.logout_user(token_data=token_data, token_cache=token_cache)
    logger.info("Logout completed successfully.")
    return {"detail": "Logged out successfully"}


@router.get("/me", response_model=UserResponseDTO)
async def read_user_route(
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
) -> UserResponseDTO:
    """
    Retrieve the current active user's information.
    """
    return UserResponseDTO.model_validate(current_active_user)


@router.post("/confirm_email")
async def confirm_email_route(
    service: Annotated[UserService, Depends(service_dependency)],
    confirmation_token: Annotated[str, Query(..., description="Email confirmation token.")],
) -> dict:
    """
    Confirm a user's email using the provided confirmation token.
    """
    logger.info("Received email confirmation request.")
    await service.confirm_email(confirmation_token=confirmation_token)
    logger.info("Email confirmed successfully.")
    return {"detail": "Email confirmed successfully."}


@router.post("/reset_password_request")
async def reset_password_request_route(
    email: Annotated[EmailStr, Query(..., description="Email address for password reset.")],
    background_tasks: BackgroundTasks,
    service: Annotated[UserService, Depends(service_dependency)],
) -> dict:
    """
    Initiate a password reset request for the provided email.
    Returns a success message regardless of whether the user exists.
    """
    try:
        logger.info("Received password reset request.")
        await service.reset_password_request(email=email, background_tasks=background_tasks)
        logger.info("Password reset request successful.")
        return {"detail": "Password reset instructions have been sent to your registered email address."}
    except UserNotFoundException as e:
        logger.error("Password reset request: {}", str(e))
        # Don't push any error message to user if user does not exist. Just act normal :)
        # Return success to avoid leaking whether the email exists.
        return {"detail": "Password reset instructions have been sent to your registered email address."}


@router.post("/reset_password")
async def reset_password_route(
    reset_token: Annotated[str, Body(..., description="The token received for password reset.")],
    new_password: Annotated[str, Body(..., description="The new password to be set for the user account.")],
    service: Annotated[UserService, Depends(service_dependency)],
) -> dict:
    """
    Reset the user's password using the provided reset token and new password.
    """
    logger.info("Received password reset request.")
    # if not reset_token:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Reset token is not valid.",
    #     )

    await service.reset_password(reset_token=reset_token, new_password=new_password)
    logger.info("Password reset successfully.")
    return {"detail": "Password reset successfully"}


@router.get("/my_challenges", response_model=PaginationResponse)
async def my_challenges_route(
    service: Annotated[UserService, Depends(service_dependency)],
    challenge_service: Annotated[ChallengeService, Depends(challenge_service_dependency)],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    limit: int | None = None,
    offset: int | None = None,
) -> PaginationResponse[Optional[TaskModelBaseOutputDTO]]:
    """
    Retrieve challenges associated with the current user.

    """

    entity_list, total_pages, total_records = await challenge_service.list(
        limit=limit, offset=offset, search_filters={"challenge_owner_id": current_active_user.id}, sort_by="challenge_created_time", sort_desc=True
    )
    return PaginationResponse(
        total_pages=total_pages,
        total_records=total_records,
        content=entity_list,
    )


@router.get("/my_tasks", response_model=PaginationResponse)
async def my_tasks_route(
    service: Annotated[UserService, Depends(service_dependency)],
    task_service: Annotated[UserService, Depends(task_service_dependency)],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    limit: int | None = None,
    offset: int | None = None,
) -> PaginationResponse[Optional[TaskModelBaseOutputDTO]]:
    """
    Retrieve tasks associated with the current user.

    """

    entity_list, total_pages, total_records = await task_service.list(
        limit=limit, offset=offset, search_filters={"task_owner_id": current_active_user.id}
    )
    return PaginationResponse(
        total_pages=total_pages,
        total_records=total_records,
        content=entity_list,
    )
