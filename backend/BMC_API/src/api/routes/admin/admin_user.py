# backend/BMC_API/src/api/routes/admin_user.py
# Exceptions raised the routes here will be caught by the global exception handlers.

from datetime import datetime
from typing import Annotated, Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Path, status
from loguru import logger

# from pydantic import EmailStr
from BMC_API.src.api.dependencies.route_dependencies import get_repository, get_service
from BMC_API.src.api.dependencies.schemas import (
    BulkOperationResponse,
    PaginationResponse,
    SearchRequest,
)
from BMC_API.src.api.schemas.user_schema import UserInDB
from BMC_API.src.application.dto.user_dto import (
    UserCreateAdminDTO,
    UserResponseAdminDTO,
    UserUpdateAdminDTO,
)
from BMC_API.src.application.interfaces.authentication import (
    ensure_current_active_user,
    validate_active_user_password_dependency,
)
from BMC_API.src.application.interfaces.authorization import RoleChecker
from BMC_API.src.application.use_cases.admin_use_cases import AdminUserService

# from BMC_API.src.application.use_cases.user_use_cases import UserService
from BMC_API.src.domain.value_objects.enums.user_enums import Roles
from BMC_API.src.infrastructure.persistence.dao.user_dao import SQLAlchemyUserRepository

router = APIRouter(
    dependencies=[Depends(RoleChecker([Roles.ADMIN]))]
)  # IMPORTANT: dependency injection among al endpoints here for role checking


# Dependency functions
repository_dependency = get_repository(SQLAlchemyUserRepository)
service_dependency = get_service(AdminUserService, repository_dependency, dto_class=UserResponseAdminDTO)


# Admin routes for user management
@router.get("/{id:int}", response_model=Optional[UserResponseAdminDTO])
async def get_user_route_admin(
    id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
    service: Annotated[AdminUserService, Depends(service_dependency)],
) -> Optional[UserResponseAdminDTO]:
    logger.info(f"Received admin request to get user with id: {id}")
    user: UserResponseAdminDTO = await service.get(id=id)
    if not user:
        logger.info(f"User with id: {id} not found")
    else:
        logger.info(f"User with id: {id} retrieved")
    return user


@router.post("/all", response_model=PaginationResponse, response_model_exclude_none=True)
async def list_users_route_admin(
    service: Annotated[AdminUserService, Depends(service_dependency)],
    limit: int | None = None,
    offset: int | None = None,
    search_request: SearchRequest | None = None,
    sort_by: str | None = "id",
    sort_desc: bool | None = False,
) -> PaginationResponse[Optional[UserResponseAdminDTO]]:
    search_filters = search_request.search_filters if search_request and search_request.search_filters else None
    output_filters = search_request.output_filters if search_request and search_request.output_filters else None

    user_list, total_pages, total_records = await service.list(
        limit=limit,
        offset=offset,
        search_filters=search_filters,
        output_filters=output_filters,
        sort_by=sort_by,
        sort_desc=sort_desc,
    )
    return PaginationResponse(
        total_pages=total_pages,
        total_records=total_records,
        content=user_list,
    )


@router.post("/create", response_model=UserResponseAdminDTO, status_code=status.HTTP_201_CREATED)
async def create_user_route_admin(
    user: Annotated[
        UserCreateAdminDTO,
        Body(
            ...,
            description="User creation details, including email, password, and other required fields.",
        ),
    ],
    background_tasks: BackgroundTasks,
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[AdminUserService, Depends(service_dependency)],
) -> UserResponseAdminDTO:
    """
    Create a new user. Prevents account creation if a user is already logged in.
    """
    logger.info(f"Received admin request to create user with email: {user.email}")

    created_user: UserResponseAdminDTO = await service.create_user(user_create=user, background_tasks=background_tasks)
    logger.info(f"User {created_user.id} created successfully by {current_active_user.email}.")
    return created_user


@router.put(
    "/update/{id:int}",
    response_model=UserResponseAdminDTO,
    response_model_exclude_none=True,
)
async def update_user_route_admin(
    id: Annotated[int, Path(title="The ID of the item to update", ge=1)],
    model_update: Annotated[
        UserUpdateAdminDTO,
        Body(..., description="The updated user details (e.g., new email, name, etc.)."),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[AdminUserService, Depends(service_dependency)],
) -> UserResponseAdminDTO:
    """
    Update an existing user's details with admin rights. The user ID is taken from the URI.
    """

    logger.info(f"Received admin request to update user with id: {id}")
    entity_data = model_update.model_dump()
    entity_data["modified_time"] = datetime.now()
    updated_user = await service.update(id=id, user_update=entity_data)
    logger.info(f"User with id {id} updated successfully by {current_active_user.email}.")
    return updated_user


@router.put("/bulk-update", response_model=BulkOperationResponse[UserResponseAdminDTO])
async def bulk_update_users_route_admin(
    updates: Annotated[
        List[Dict[str, Any]],
        Body(
            examples=[[{"id": 1, "field": "string"}, {"id": 2, "field": "string"}]],
            title="The updated model details (e.g., name, etc.).",
            description="List of user updates. Each item should contain 'id' and update data (column names as keys and values).",
        ),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[AdminUserService, Depends(service_dependency)],
) -> BulkOperationResponse[UserResponseAdminDTO]:
    """
    Bulk update multiple users' details with admin rights.
    Each update in the list must contain the user ID and the fields to update.
    """
    logger.info(f"Received admin request to bulk update {len(updates)} users")
    [entity_data.update({"modified_time": datetime.now()}) for entity_data in updates]
    results = await service.update_bulk(updates=updates)
    logger.info(results.detail, f"Requested by {current_active_user.email}.")
    return results


@router.delete(
    "/delete/{id:int}",
    summary="⚠️ Delete a user",
    description="Delete a user with the specified ID. Requires admin privileges and password confirmation for security.",
    response_description="Confirmation of successful deletion",
)
async def delete_user_route_admin(
    id: Annotated[int, Path(title="The ID of the item to delete", ge=1)],
    current_active_user: Annotated[UserInDB, Depends(validate_active_user_password_dependency)],
    service: Annotated[AdminUserService, Depends(service_dependency)],
) -> dict:
    """
    Delete user from database with admin rights.
    The ID of entity to be deleted is taken from the URI.
    """
    logger.info(f"Received admin request to delete user with id: {id}")
    await service.delete(id=id)
    logger.info(f"User with id: {id} deleted successfully by {current_active_user.email}.")
    return {"detail": "User deleted"}


@router.delete(
    "/bulk-delete",
    response_model=BulkOperationResponse[Any],
    summary="⚠️ Delete multiple users",
    description="Delete multiple users with the specified IDs. Requires admin privileges and password confirmation for security.",
    response_description="Confirmation of successful deletion",
)
async def bulk_delete_users_route_admin(
    ids: Annotated[
        List[int],
        Body(..., description="List of user IDs to be deleted.", example=[1, 2, 3]),
    ],
    current_active_user: Annotated[UserInDB, Depends(validate_active_user_password_dependency)],
    service: Annotated[AdminUserService, Depends(service_dependency)],
) -> BulkOperationResponse[Any]:
    """
    Delete multiple users from database with admin rights.
    The IDs of users to be deleted must be provided as a list.
    """
    logger.info(f"Received admin request to bulk delete {len(ids)} users")
    results = await service.delete_bulk(ids=ids)
    logger.info(results.detail, f"Requested by {current_active_user.email}.")
    return results
