# backend/BMC_API/src/api/routes/challenge.py
# Exceptions raised the routes here will be caught by the global exception handlers.

from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Path, status
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger

from BMC_API.src.api.dependencies.route_dependencies import get_repository
from BMC_API.src.api.schemas.user_schema import UserInDB
from BMC_API.src.application.dependencies import get_challenge_service
from BMC_API.src.application.dto.challenge_dto import (
    ChallengeModelBaseOutputDTO,
    ChallengeModelCreateDTO,
    ChallengeModelUpdateDTO,
)
from BMC_API.src.application.interfaces.authentication import (
    ensure_current_active_user,
    validate_active_user_password_dependency,
)
from BMC_API.src.application.interfaces.authorization import (
    RoleChecker,
    ownership_checker_dependency,
)
from BMC_API.src.application.use_cases.challenge_use_cases import ChallengeService
from BMC_API.src.core.exceptions import ConferenceLockedException
from BMC_API.src.domain.value_objects.enums.user_enums import Roles
from BMC_API.src.infrastructure.persistence.dao.challenge_dao import (
    SQLAlchemyChallengeRepository,
)

# Dependency functions
repository_dependency = get_repository(SQLAlchemyChallengeRepository)


ownership_check = ownership_checker_dependency(
    service_class=ChallengeService,
    model_id_field="challenge_owner_id",
    repository_dependency=repository_dependency,
    get_model_id=lambda id: int(id),
)

# Router
router = APIRouter(
    dependencies=[Depends(RoleChecker([Roles.ORGANIZER]))]
)  # IMPORTANT: dependency injection among all endpoints here for role checking


# Routes
@router.get("/{id:int}", response_model=Optional[ChallengeModelBaseOutputDTO])
async def get_challenge_route(
    id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
    service: Annotated[ChallengeService, Depends(get_challenge_service)],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    _ownership: Annotated[bool, Depends(ownership_check)],
) -> Optional[ChallengeModelBaseOutputDTO]:
    """
    Retrieve a challenge by its ID.

    This endpoint fetches the details of a entity identified by its unique ID.
    If the entity exists, it returns the entity data as a ChallengeModelBaseOutputDTO.
    If not found, it returns None.

    **Parameters:**

    * `id (int)`: The unique identifier of the challenge to retrieve. Must be a positive integer.

    **Returns:**

    * `Optional[ChallengeModelBaseOutputDTO]`: The challenge details if found; otherwise, None.
    """
    logger.info(f"Received request to get challenge with id {id} by {current_active_user.email}")
    entity = await service.get(id=id)
    logger.info(f"Challenge with id {id} retrieved successfully by {current_active_user.email}.")
    return entity


@router.post("/create", response_model=ChallengeModelBaseOutputDTO, status_code=status.HTTP_201_CREATED)
async def create_challenge_route(
    conference_id: int,
    model_create: Annotated[
        ChallengeModelCreateDTO,
        Body(
            ...,
            description="Challenge creation details.",
        ),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[ChallengeService, Depends(get_challenge_service)],
    # conference_service: Annotated[ChallengeService, Depends(conference_service_dependency)],
) -> ChallengeModelBaseOutputDTO:
    """
    Create a new challenge.
    """
    logger.info(f"Received request to create challenge by {current_active_user.email}")

    # Check if conference is open for submissions
    conference_raw = await service.conference_service.get_raw(id=conference_id)
    is_open_for_submissions = getattr(conference_raw, "is_open_for_submissions", None)

    if not is_open_for_submissions:
        raise ConferenceLockedException

    entity_data = model_create.model_dump()
    entity_data["challenge_owner_id"] = current_active_user.id
    entity_data["challenge_created_time"] = datetime.now()
    entity_data["challenge_conference_id"] = conference_id
    created = await service.create(model_create=entity_data)
    logger.info(f"Challenge {created.id} created successfully by {current_active_user.email}.")
    return created


@router.put("/{id:int}/update", response_model=ChallengeModelBaseOutputDTO)
async def update_challenge_route(
    id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
    model_update: Annotated[
        ChallengeModelUpdateDTO,
        Body(..., description="The updated challenge details."),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    _ownership: Annotated[bool, Depends(ownership_check)],
    service: Annotated[ChallengeService, Depends(get_challenge_service)],
    # conference_service: Annotated[ChallengeService, Depends(conference_service_dependency)],
) -> ChallengeModelBaseOutputDTO:
    """Update an existing challenge's details."""

    logger.info(f"Received request to update challenge with id {id} by {current_active_user.email}")

    # Check if conference is open for submissions
    challenge_raw = await service.get_raw(id=id)

    if not challenge_raw.is_allowed_for_further_editing:
        conference_raw = await service.conference_service.get_raw(id=challenge_raw.challenge_conference_id)
        is_open_for_submissions = getattr(conference_raw, "is_open_for_submissions", None)

        if not is_open_for_submissions:
            raise ConferenceLockedException

    entity_data = model_update.model_dump()
    updated = await service.update_challenge(id=id, model_update=entity_data)
    logger.info(f"Challenge with id {updated.id} updated successfully by {current_active_user.email}.")
    return updated


@router.delete(
    "/{id:int}/delete",
    summary="⚠️ Delete a challenge",
    description="Delete a challenge with the specified ID. Requires ownership.",
    response_description="Confirmation of successful deletion",
)
async def delete_challenge_route(
    id: Annotated[int, Path(title="The ID of the item to delete", ge=1)],
    current_active_user: Annotated[UserInDB, Depends(validate_active_user_password_dependency)],
    service: Annotated[ChallengeService, Depends(get_challenge_service)],
    _ownership: Annotated[bool, Depends(ownership_check)],
) -> dict:
    """
    Delete challenge from database.
    The ID of entity to be deleted is taken from the URI.
    """
    logger.info(f"Received request to delete challenge with id {id} by {current_active_user.email}")
    await service.prune_challenge(id=id)
    logger.info(f"Challenge with id: {id} deleted successfully by {current_active_user.email}.")
    return {"detail": "Challenge deleted"}


@router.put("/{id:int}/submit")
async def submit_challenge_route(
    id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
    background_tasks: BackgroundTasks,
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    _ownership: Annotated[bool, Depends(ownership_check)],
    service: Annotated[ChallengeService, Depends(get_challenge_service)],
) -> JSONResponse:
    """Submit a challenge."""

    logger.info(f"Received request to submit challenge with id {id} by {current_active_user.email}")

    # Check if conference is open for submissions
    challenge_raw = await service.get_raw(id=id)

    if not challenge_raw.is_allowed_for_further_editing:
        conference_raw = await service.conference_service.get_raw(id=challenge_raw.challenge_conference_id)
        is_open_for_submissions = getattr(conference_raw, "is_open_for_submissions", None)

        if not is_open_for_submissions:
            raise ConferenceLockedException

    await service.submit_challenge(
        id=id,
        background_tasks=background_tasks,
        send_notification_emails=True,
    )

    logger.info(f"Challenge with id {id} submit successfully by {current_active_user.email}.")
    return JSONResponse(
        status_code=200,
        content={"message": "Challenge successfully submitted. Challenge document is ready to download."},
    )


@router.get(
    "/{id}/download",
    summary="Download challenge file",
    description="Download challenge file if the challenge is submitted. Requires ownership.",
    response_description="`FileResponse` including Challenge PDF file",
    responses={
        "200": {
            "description": "Successful Response",
            "content-type": {"application/pdf": {"schema": {}}},
        },
        "422": {
            "description": "Validation Error",
            "content-type": {"application/json": {"schema": {"$ref": "#/components/schemas/HTTPValidationError"}}},
        },
    },
)
async def download_challenge_document_route(
    id: Annotated[int, Path(title="The ID of the item to delete", ge=1)],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[ChallengeService, Depends(get_challenge_service)],
    _ownership: Annotated[bool, Depends(ownership_check)],
) -> FileResponse:
    logger.info(f"Received request to download challenge with id {id} by {current_active_user.email}")
    file = await service.download_challenge(id=id)
    logger.info(f"Challenge with id {id} retrieved successfully by {current_active_user.email}.")
    return file
