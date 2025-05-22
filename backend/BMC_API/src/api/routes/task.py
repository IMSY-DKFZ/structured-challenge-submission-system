# backend/BMC_API/src/api/routes/task.py
# Exceptions raised the routes here will be caught by the global exception handlers.

from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger

from BMC_API.src.api.dependencies.route_dependencies import get_repository, get_service
from BMC_API.src.api.schemas.user_schema import UserInDB
from BMC_API.src.application.dto.challenge_dto import ChallengeModelBaseOutputDTO
from BMC_API.src.application.dto.task_dto import (
    TaskModelBaseOutputDTO,
    TaskModelCreateDTO,
    TaskModelUpdateDTO,
)
from BMC_API.src.application.interfaces.authentication import ensure_current_active_user
from BMC_API.src.application.interfaces.authorization import (
    RoleChecker,
    ownership_checker_dependency,
)
from BMC_API.src.application.use_cases.challenge_use_cases import ChallengeService
from BMC_API.src.application.use_cases.task_use_cases import TaskService
from BMC_API.src.core.exceptions import ConferenceLockedException
from BMC_API.src.domain.value_objects.enums.user_enums import Roles
from BMC_API.src.infrastructure.persistence.dao.challenge_dao import (
    SQLAlchemyChallengeRepository,
)
from BMC_API.src.infrastructure.persistence.dao.task_dao import SQLAlchemyTaskRepository

# Dependency functions
repository_dependency = get_repository(SQLAlchemyTaskRepository)
service_dependency = get_service(TaskService, repository_dependency, dto_class=TaskModelBaseOutputDTO)
challenge_repository_dependency = get_repository(SQLAlchemyChallengeRepository)
challenge_service_dependency = get_service(
    ChallengeService, challenge_repository_dependency, dto_class=ChallengeModelBaseOutputDTO
)

ownership_check = ownership_checker_dependency(
    service_class=TaskService,
    model_id_field="task_owner_id",
    repository_dependency=repository_dependency,
    get_model_id=lambda id: int(id),
)

# Router
router = APIRouter(
    dependencies=[Depends(RoleChecker([Roles.ORGANIZER]))]
)  # IMPORTANT: dependency injection among all endpoints here for role checking


# Routes
@router.get("/{id:int}", response_model=Optional[TaskModelBaseOutputDTO])
async def get_task_route(
    id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
    service: Annotated[TaskService, Depends(service_dependency)],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    _ownership: Annotated[bool, Depends(ownership_check)],
) -> Optional[TaskModelBaseOutputDTO]:
    """
    Retrieve a task by its ID.

    This endpoint fetches the details of a entity identified by its unique ID.
    If the entity exists, it returns the entity data as a TaskModelBaseOutputDTO.
    If not found, it returns None.

    **Parameters:**

    * `id (int)`: The unique identifier of the task to retrieve. Must be a positive integer.

    **Returns:**

    * `Optional[TaskModelBaseOutputDTO]`: The task details if found; otherwise, None.
    """
    logger.info(f"Received request to get task with id {id} by {current_active_user.email}")
    entity = await service.get(id=id)
    logger.info(f"Task with id {id} retrieved successfully by {current_active_user.email}.")
    return entity


@router.post("/create", response_model=TaskModelBaseOutputDTO, status_code=status.HTTP_201_CREATED)
async def create_task_route(
    challenge_id: int,
    model_create: Annotated[
        TaskModelCreateDTO,
        Body(
            ...,
            description="Task creation details.",
        ),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[TaskService, Depends(service_dependency)],
    challenge_service: Annotated[ChallengeService, Depends(challenge_service_dependency)],
) -> TaskModelBaseOutputDTO:
    """
    Create a new task.
    """
    logger.info(f"Received request to create task by {current_active_user.email}")

    # Check if conference is open for submissions
    challenge_raw = await challenge_service.get_raw(id=challenge_id)
    conference_raw = getattr(challenge_raw, "challenge_conference", None)
    is_open_for_submissions = getattr(conference_raw, "is_open_for_submissions", None)

    if not is_open_for_submissions:
        raise ConferenceLockedException

    entity_data = model_create.model_dump()
    entity_data["task_owner_id"] = current_active_user.id
    entity_data["task_challenge_id"] = challenge_id
    entity_data["task_created_time"] = datetime.now()
    created = await service.create(model_create=entity_data)
    logger.info(f"Task {created.id} created successfully by {current_active_user.email}.")
    return created


@router.put("/{id:int}/update", response_model=TaskModelBaseOutputDTO)
async def update_task_route(
    id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
    model_update: Annotated[
        TaskModelUpdateDTO,
        Body(..., description="The updated task details."),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    _ownership: Annotated[bool, Depends(ownership_check)],
    service: Annotated[TaskService, Depends(service_dependency)],
    challenge_service: Annotated[ChallengeService, Depends(challenge_service_dependency)],
) -> TaskModelBaseOutputDTO:
    """Update an existing task's details."""

    logger.info(f"Received request to update task with id {id} by {current_active_user.email}")

    # Check if conference is open for submissions
    task_raw = await service.get_raw(id=id)
    challenge_raw = getattr(task_raw, "task_challenge", None)

    if not challenge_raw.is_allowed_for_further_editing:
        conference_raw = getattr(challenge_raw, "challenge_conference", None)
        is_open_for_submissions = getattr(conference_raw, "is_open_for_submissions", None)

        if not is_open_for_submissions:
            raise ConferenceLockedException

    entity_data = model_update.model_dump()
    updated = await service.update_task(id=id, model_update=entity_data)
    logger.info(f"Task with id {updated.id} updated successfully by {current_active_user.email}.")
    return updated


@router.delete(
    "/{id:int}/delete",
    summary="⚠️ Delete a task",
    description="Delete a task with the specified ID. Requires ownership.",
    response_description="Confirmation of successful deletion",
)
async def delete_task_route(
    id: Annotated[int, Path(title="The ID of the item to delete", ge=1)],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[TaskService, Depends(service_dependency)],
    _ownership: Annotated[bool, Depends(ownership_check)],
) -> dict:
    """
    Delete task from database.
    The ID of entity to be deleted is taken from the URI.
    """
    logger.info(f"Received request to delete task with id {id} by {current_active_user.email}")
    await service.delete(id=id)
    logger.info(f"Task with id: {id} deleted successfully by {current_active_user.email}.")
    return {"detail": "Task deleted"}
