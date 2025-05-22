# backend/BMC_API/src/api/routes/admin/admin_task.py
# Exceptions raised the routes here will be caught by the global exception handlers.

from datetime import datetime
from typing import Annotated, Any, Dict, List, Optional

from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger

from BMC_API.src.api.dependencies.route_dependencies import get_repository, get_service
from BMC_API.src.api.dependencies.schemas import (
    BulkOperationResponse,
    PaginationResponse,
    SearchRequest,
)
from BMC_API.src.api.schemas.user_schema import UserInDB
from BMC_API.src.application.dto.task_dto import (
    TaskHistoryModelDTO,
    TaskInputAdminDTO,
    TaskResponseAdminDTO,
    TaskUpdateAdminDTO,
)
from BMC_API.src.application.interfaces.authentication import (
    ensure_current_active_user,
    validate_active_user_password_dependency,
)
from BMC_API.src.application.interfaces.authorization import RoleChecker
from BMC_API.src.application.use_cases.task_history_use_cases import TaskHistoryService
from BMC_API.src.application.use_cases.task_use_cases import TaskService
from BMC_API.src.domain.value_objects.enums.user_enums import Roles
from BMC_API.src.infrastructure.persistence.dao.task_dao import SQLAlchemyTaskRepository
from BMC_API.src.infrastructure.persistence.dao.task_history_dao import (
    SQLAlchemyTaskHistoryRepository,
)

# Dependency functions
repository_dependency = get_repository(SQLAlchemyTaskRepository)
service_dependency = get_service(TaskService, repository_dependency, dto_class=TaskResponseAdminDTO)

task_history_repository_dependency = get_repository(SQLAlchemyTaskHistoryRepository)
task_history_service_dependency = get_service(
    TaskHistoryService, task_history_repository_dependency, dto_class=TaskResponseAdminDTO
)


# Router
router = APIRouter(
    dependencies=[Depends(RoleChecker([Roles.ADMIN]))]
)  # IMPORTANT: dependency injection among all endpoints here for role checking


# Routes
@router.get("/{id:int}", response_model=TaskResponseAdminDTO)
async def get_task_route_admin(
    id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
    service: Annotated[TaskService, Depends(service_dependency)],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
) -> Optional[TaskResponseAdminDTO]:
    """
    Retrieve a task by its ID.

    This endpoint fetches the details of a entity identified by its unique ID.
    If the entity exists, it returns the entity data as a TaskResponseAdminDTO.
    If not found, it returns None.

    **Parameters:**

    * `id (int)`: The unique identifier of the task to retrieve. Must be a positive integer.

    **Returns:**

    * `Optional[TaskResponseAdminDTO]`: The task details if found; otherwise, None.
    """
    logger.info(f"Received admin request to get task with id {id} by {current_active_user.email}")
    entity = await service.get(id=id)
    logger.info(f"Task with id {id} retrieved successfully by {current_active_user.email}.")
    return entity


@router.post("/all", response_model=PaginationResponse, response_model_exclude_none=True)
async def list_tasks_route_admin(
    service: Annotated[TaskService, Depends(service_dependency)],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    limit: int | None = None,
    offset: int | None = None,
    search_request: SearchRequest | None = None,
    sort_by: str | None = "id",
    sort_desc: bool | None = False,
) -> PaginationResponse[Optional[TaskResponseAdminDTO]]:
    """
    Retrieve a paginated list of tasks for admin users.

    This endpoint allows an admin user to fetch a list of tasks with support for pagination,
    optional filtering, and sorting. The search_request may include search filters and output filters
    to refine the query. The response is structured as a PaginationResponse containing the list of
    task entities along with metadata such as total pages and total records.

    **Parameters:**

    * `limit (Optional[int])`: Maximum number of records to return. Defaults to None.

    * `offset (Optional[int])`: The starting index for the records to return. Defaults to None.

    * `search_request (Optional[SearchRequest])`: An object that may contain:
        * `search_filters`: Conditions for filtering the task records.

        * `output_filters`: Fields to include in the response.
    * `sort_by (Optional[str])`: The field name to sort the results by (default is "id").

    * `sort_desc (Optional[bool])`: Determines if sorting should be in descending order (default is False).

    **Returns:**

    * `PaginationResponse`: A response object containing:

        * `total_pages`: Total number of pages available.

        * `total_records`: Total number of task records matching the query.

        * `content`: A list of task entities for the current page.
    """
    logger.info(f"Received admin request to get multiple entities by {current_active_user.email}")
    search_filters = search_request.search_filters if search_request and search_request.search_filters else None
    output_filters = search_request.output_filters if search_request and search_request.output_filters else None

    entities, total_pages, total_records = await service.list(
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
        content=entities,
    )


@router.post("/create", response_model=TaskResponseAdminDTO, status_code=status.HTTP_201_CREATED)
async def create_task_route_admin(
    challenge_id: int,
    model_create: Annotated[
        TaskInputAdminDTO,
        Body(
            ...,
            description="Task creation details.",
        ),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[TaskService, Depends(service_dependency)],
) -> TaskResponseAdminDTO:
    """
    Create a new task.
    """
    logger.info(f"Received request to create task by {current_active_user.email}")

    entity_data = model_create.model_dump()
    entity_data["task_owner_id"] = (
        entity_data["task_owner_id"] if entity_data["task_owner_id"] else current_active_user.id
    )
    entity_data["task_challenge_id"] = challenge_id
    entity_data["version"] = entity_data["version"] if entity_data["version"] else 1
    entity_data["task_locked"] = entity_data["task_locked"] if entity_data["task_locked"] else False
    entity_data["task_created_time"] = datetime.now()
    created = await service.create(model_create=entity_data)
    logger.info(f"Task {created.id} created successfully by {current_active_user.email}.")
    return created


@router.put("/{id:int}/update", response_model=TaskResponseAdminDTO)
async def update_task_route_admin(
    id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
    model_update: Annotated[
        TaskUpdateAdminDTO,
        Body(..., description="The updated task details."),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[TaskService, Depends(service_dependency)],
) -> TaskResponseAdminDTO:
    """Update an existing task's details."""
    logger.info(f"Received admin request to update task with id {id} by {current_active_user.email}")

    entity_data = model_update.model_dump()
    entity_data["task_modified_time"] = datetime.now()
    updated = await service.update_task(id=id, model_update=entity_data)
    logger.info(f"Task with id {updated.id} updated successfully by {current_active_user.email}.")
    return updated


@router.put("/bulk-update", response_model=BulkOperationResponse[TaskResponseAdminDTO])
async def bulk_update_tasks_route_admin(
    updates: Annotated[
        List[Dict[str, Any]],
        Body(
            examples=[[{"id": 1, "field": "string"}, {"id": 2, "field": "string"}]],
            title="The updated task details.",
            description="List of task updates. Each item should contain 'id' and update data (column names as keys and values).",
        ),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[TaskService, Depends(service_dependency)],
) -> BulkOperationResponse[TaskResponseAdminDTO]:
    """
    Bulk update multiple tasks' details with admin rights.
    Each update in the list must contain the task ID and the fields to update.
    """
    logger.info(f"Received admin request to bulk update {len(updates)} tasks  by {current_active_user.email}.")
    result = await service.update_task_bulk(updates=updates)
    logger.info(result.detail, "Bulk updates successful.")
    return result


@router.delete(
    "/{id:int}/delete",
    summary="⚠️ Delete a task",
    description="Delete a task with the specified ID. Requires ownership.",
    response_description="Confirmation of successful deletion",
)
async def delete_task_route_admin(
    id: Annotated[int, Path(title="The ID of the item to delete", ge=1)],
    current_active_user: Annotated[UserInDB, Depends(validate_active_user_password_dependency)],
    service: Annotated[TaskService, Depends(service_dependency)],
) -> dict:
    """
    Delete task from database.
    The ID of entity to be deleted is taken from the URI.
    """
    logger.info(f"Received admin request to delete task with id {id} by {current_active_user.email}")
    await service.delete(id=id)
    logger.info(f"Task with id {id} deleted successfully by {current_active_user.email}.")
    return {"detail": "Task deleted"}


@router.delete(
    "/bulk-delete",
    response_model=BulkOperationResponse[Any],
    summary="⚠️ Delete multiple tasks",
    description="Delete multiple tasks with the specified IDs. Requires admin privileges and password confirmation for security.",
    response_description="Confirmation of successful deletion",
)
async def bulk_delete_tasks_route_admin(
    ids: Annotated[
        List[int],
        Body(..., description="List of task IDs to be deleted.", example=[1, 2, 3]),
    ],
    current_active_user: Annotated[UserInDB, Depends(validate_active_user_password_dependency)],
    service: Annotated[TaskService, Depends(service_dependency)],
) -> BulkOperationResponse[Any]:
    """
    Delete multiple tasks from database with admin rights.
    The IDs of tasks to be deleted must be provided as a list.
    """
    logger.info(f"Received admin request to bulk delete {len(ids)} tasks  by {current_active_user.email}.")
    result = await service.delete_bulk(ids=ids)
    logger.info(result.detail, "Bulk delete successful.")
    return result


@router.get(
    "/{id:int}/histories",
    response_model=PaginationResponse,
    summary="Get histories of task between status of DRAFT_SUBMITTED, REVISION_SUBMITTED, ACCEPT",
)
async def get_task_history_admin(
    id: int,
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[TaskService, Depends(service_dependency)],
) -> PaginationResponse[Optional[List[TaskHistoryModelDTO]]]:
    logger.info(f"Received admin request to get histories of task with id {id} by {current_active_user.email}")

    entities, total_pages, total_records = await service.task_histories(id=id)
    logger.info("Task histories fetched successfully.")
    return PaginationResponse(
        total_pages=total_pages,
        total_records=total_records,
        content=entities,
    )


@router.delete(
    "/{id:int}/delete_history",
    summary="⚠️ Delete a task history",
    description="Delete a task history with the specified ID. Requires ownership.",
    response_description="Confirmation of successful deletion",
)
async def delete_task_history_route_admin(
    id: Annotated[int, Path(title="The ID of the item to delete", ge=1)],
    current_active_user: Annotated[UserInDB, Depends(validate_active_user_password_dependency)],
    service: Annotated[TaskService, Depends(service_dependency)],
    task_history_service: Annotated[TaskHistoryService, Depends(task_history_service_dependency)],
) -> dict:
    """
    Delete task history from database.
    The ID of entity to be deleted is taken from the URI.
    """
    logger.info(f"Received admin request to delete task history with id {id} by {current_active_user.email}")
    await task_history_service.delete(id=id)
    logger.info(f"Task history with id {id} deleted successfully by {current_active_user.email}.")
    return {"detail": "Task history deleted"}
