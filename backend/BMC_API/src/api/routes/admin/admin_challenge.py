# backend/BMC_API/src/api/routes/admin/admin_challenge.py
# Exceptions raised the routes here will be caught by the global exception handlers.

from datetime import datetime
from typing import Annotated, Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Path, Query, status
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from loguru import logger

# from BMC_API.src.api.dependencies.route_dependencies import get_repository, get_service
from BMC_API.src.api.dependencies.schemas import (
    BulkOperationResponse,
    PaginationResponse,
    SearchRequest,
)
from BMC_API.src.api.schemas.user_schema import UserInDB
from BMC_API.src.application.dependencies import get_challenge_service_admin
from BMC_API.src.application.dto.challenge_dto import (
    ChallengeHistoryModelDTO,
    ChallengeInputAdminDTO,
    ChallengeModelStatusUpdateDTO,
    ChallengeResponseAdminDTO,
    ChallengeUpdateAdminDTO,
)
from BMC_API.src.application.interfaces.authentication import (
    ensure_current_active_user,
    validate_active_user_password_dependency,
)
from BMC_API.src.application.interfaces.authorization import RoleChecker
from BMC_API.src.application.use_cases.challenge_use_cases import ChallengeService
from BMC_API.src.domain.value_objects.enums.user_enums import Roles

# Router
router = APIRouter(
    dependencies=[Depends(RoleChecker([Roles.ADMIN]))]
)  # IMPORTANT: dependency injection among all endpoints here for role checking


# Routes
@router.get("/{id:int}", response_model=ChallengeResponseAdminDTO)
async def get_challenge_route_admin(
    id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
) -> Optional[ChallengeResponseAdminDTO]:
    """
    Retrieve a challenge by its ID.

    This endpoint fetches the details of a entity identified by its unique ID.
    If the entity exists, it returns the entity data as a ChallengeResponseAdminDTO.
    If not found, it returns None.

    **Parameters:**

    * `id (int)`: The unique identifier of the challenge to retrieve. Must be a positive integer.

    **Returns:**

    * `Optional[ChallengeResponseAdminDTO]`: The challenge details if found; otherwise, None.
    """
    logger.info(f"Received admin request to get challenge with id {id} by {current_active_user.email}")
    entity = await service.get(id=id)
    logger.info(f"Challenge with id {id} retrieved successfully by {current_active_user.email}.")
    return entity


@router.post("/all", response_model=PaginationResponse, response_model_exclude_none=True)
async def list_challenges_route_admin(
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    limit: int | None = None,
    offset: int | None = None,
    search_request: SearchRequest | None = None,
    sort_by: str | None = "id",
    sort_desc: bool | None = False,
) -> PaginationResponse[Optional[ChallengeResponseAdminDTO]]:
    """
    Retrieve a paginated list of challenges for admin users.

    This endpoint allows an admin user to fetch a list of challenges with support for pagination,
    optional filtering, and sorting. The search_request may include search filters and output filters
    to refine the query. The response is structured as a PaginationResponse containing the list of
    challenge entities along with metadata such as total pages and total records.

    **Parameters:**

    * `limit (Optional[int])`: Maximum number of records to return. Defaults to None.

    * `offset (Optional[int])`: The starting index for the records to return. Defaults to None.

    * `search_request (Optional[SearchRequest])`: An object that may contain:
        * `search_filters`: Conditions for filtering the challenge records.

        * `output_filters`: Fields to include in the response.
    * `sort_by (Optional[str])`: The field name to sort the results by (default is "id").

    * `sort_desc (Optional[bool])`: Determines if sorting should be in descending order (default is False).

    **Returns:**

    * `PaginationResponse`: A response object containing:

        * `total_pages`: Total number of pages available.

        * `total_records`: Total number of challenge records matching the query.

        * `content`: A list of challenge entities for the current page.
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


@router.post("/create", response_model=ChallengeResponseAdminDTO, status_code=status.HTTP_201_CREATED)
async def create_challenge_route_admin(
    conference_id: int,
    model_create: Annotated[
        ChallengeInputAdminDTO,
        Body(
            ...,
            description="Challenge creation details.",
        ),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
) -> ChallengeResponseAdminDTO:
    """
    Create a new challenge.
    """
    logger.info(f"Received request to create challenge by {current_active_user.email}")

    entity_data = model_create.model_dump()
    entity_data["challenge_owner_id"] = (
        entity_data["challenge_owner_id"] if entity_data["challenge_owner_id"] else current_active_user.id
    )
    entity_data["challenge_conference_id"] = conference_id
    entity_data["version"] = entity_data["version"] if entity_data["version"] else 1
    entity_data["challenge_locked"] = entity_data["challenge_locked"] if entity_data["challenge_locked"] else False
    entity_data["is_allowed_for_further_editing"] = (
        entity_data["is_allowed_for_further_editing"] if entity_data["is_allowed_for_further_editing"] else True
    )
    entity_data["challenge_created_time"] = datetime.now()
    created = await service.create(model_create=entity_data)
    logger.info(f"Challenge {created.id} created successfully by {current_active_user.email}.")
    return created


@router.put("/{id:int}/update", response_model=ChallengeResponseAdminDTO)
async def update_challenge_route_admin(
    id: Annotated[int, Path(title="The ID of the item to update", ge=1)],
    model_update: Annotated[
        ChallengeUpdateAdminDTO,
        Body(..., description="The updated challenge details."),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
) -> ChallengeResponseAdminDTO:
    """Update an existing challenge's details."""
    logger.info(f"Received admin request to update challenge with id {id} by {current_active_user.email}")

    entity_data = model_update.model_dump()
    updated = await service.update_challenge(id=id, model_update=entity_data)
    logger.info(f"Challenge with id {updated.id} updated successfully by {current_active_user.email}.")
    return updated


@router.put("/bulk-update", response_model=BulkOperationResponse[ChallengeResponseAdminDTO])
async def bulk_update_challenges_route_admin(
    updates: Annotated[
        List[Dict[str, Any]],
        Body(
            examples=[[{"id": 1, "field": "string"}, {"id": 2, "field": "string"}]],
            title="The updated challenge details.",
            description="List of challenge updates. Each item should contain 'id' and update data (column names as keys and values).",
        ),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
) -> BulkOperationResponse[ChallengeResponseAdminDTO]:
    """
    Bulk update multiple challenges' details with admin rights.
    Each update in the list must contain the challenge ID and the fields to update.
    """
    logger.info(f"Received admin request to bulk update {len(updates)} challenges  by {current_active_user.email}.")
    result = await service.update_challenge_bulk(updates=updates)
    logger.info(result.detail, "Bulk updates successful.")
    return result


@router.put("/{id:int}/status", response_model=ChallengeResponseAdminDTO)
async def update_challenge_status_route_admin(
    id: Annotated[int, Path(title="The ID of the item to update", ge=1)],
    challenge_status_object: Annotated[
        ChallengeModelStatusUpdateDTO,
        Body(
            examples=[
                {"challenge_status": "Draft"},
                {"challenge_status": "DraftUpdated"},
                {"challenge_status": "MinorRevisionRequired"},
                {"challenge_status": "Accept"},
                {"challenge_status": "Reject"},
            ],
            title="Challenge Status.",
            description="New status to apply to selected challenge and all related tasks. New status must be value of ChallengeStatus",
        ),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
    # task_service: Annotated[TaskService, Depends(task_service_dependency)],
) -> ChallengeResponseAdminDTO:
    """Update an existing challenge's details."""
    logger.info(f"Received admin request to update status of challenge with id {id} by {current_active_user.email}")
    new_status = challenge_status_object.challenge_status
    updated = await service.status(id=id, new_status=new_status)

    logger.info(f"Status of challenge with id {id} updated successfully by {current_active_user.email}.")
    return updated


@router.put("/bulk-status", response_model=BulkOperationResponse[ChallengeResponseAdminDTO])
async def bulk_update_challenge_status_route_admin(
    ids: Annotated[
        List[int],
        Body(examples=[[1, 2, 3]], title="List of Challenge IDs", description="IDs of challenges to bulk update."),
    ],
    challenge_status_object: Annotated[
        ChallengeModelStatusUpdateDTO,
        Body(
            examples=[
                {"challenge_status": "Draft"},
                {"challenge_status": "DraftUpdated"},
                {"challenge_status": "MinorRevisionRequired"},
                {"challenge_status": "Accept"},
                {"challenge_status": "Reject"},
            ],
            title="Challenge Status",
            description="New status to apply to all selected challenges and all their related tasks. New status must be value of ChallengeStatus",
        ),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
    # task_service: Annotated[TaskService, Depends(task_service_dependency)],
) -> BulkOperationResponse[ChallengeResponseAdminDTO]:
    """
    Bulk update the status of multiple challenges (and their related tasks) with a common status.
    """
    logger.info(
        f"Received admin request to bulk update status for {len(ids)} challenges by {current_active_user.email}."
    )
    new_status = challenge_status_object.challenge_status
    result = await service.bulk_status(ids=ids, new_status=new_status)
    logger.info(result)
    return result


@router.put("/{id:int}/submit")
async def submit_challenge_route_admin(
    id: Annotated[int, Path(title="The ID of the item to submit", ge=1)],
    background_tasks: BackgroundTasks,
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
    send_notification_emails: Annotated[
        bool | None,
        Query(description="Send notification emails to challenge organizers, conference chairs and system admins."),
    ] = False,
) -> JSONResponse:
    """Submit a challenge."""

    logger.info(f"Received request to submit challenge with id {id} by {current_active_user.email}")

    await service.submit_challenge(
        id=id,
        background_tasks=background_tasks,
        send_notification_emails=send_notification_emails,
    )

    logger.info(f"Challenge with id {id} submit successfully by {current_active_user.email}.")
    return JSONResponse(
        status_code=200,
        content={"message": "Challenge successfully submitted. Challenge document is ready to download."},
    )


@router.get("/{id:int}/take_snapshot")
async def take_snapshot_route_admin(
    id: Annotated[int, Path(title="The ID of the item to take snapshot", ge=1)],
    # background_tasks: BackgroundTasks,
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
) -> JSONResponse:
    """Take snapshot of a challenge and related tasks manually."""

    logger.info(f"Received request to take snapshot challenge with id {id} by {current_active_user.email}")

    await service.take_snapshot(id=id)

    logger.info(f"Snapshot created for challenge with id {id} successfully by {current_active_user.email}.")
    return JSONResponse(
        status_code=200,
        content={"message": "Snapshot created successfully."},
    )


@router.get(
    "/{id}/download",
    summary="Download challenge file",
    description="Download challenge file if the challenge is submitted.",
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
async def download_challenge_document_route_admin(
    id: Annotated[int, Path(title="The ID of the item to download", ge=1)],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
) -> FileResponse:
    logger.info(f"Received admin request to download challenge with id {id} by {current_active_user.email}")
    file = await service.download_challenge(id=id)
    logger.info(f"Challenge with id {id} retrieved successfully by {current_active_user.email}.")
    return file


@router.post(
    "/bulk-download",
    summary="Download multiple challenges",
    description="Download multiple challenges with the specified IDs. Requires admin privileges.",
    response_description="Confirmation of successful downloads",
)
async def bulk_download_challenge_document_route_admin(
    ids: Annotated[
        List[int],
        Body(..., description="List of challenge IDs to be downloaded.", example=[1, 2, 3]),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
) -> StreamingResponse:
    """
    Download multiple challenges from database with admin rights.
    The IDs of challenges to be downloaded must be provided as a list.
    """
    logger.info(f"Received admin request to bulk download {len(ids)} challenges  by {current_active_user.email}.")
    file = await service.download_challenge_bulk(ids=ids)
    logger.info("Bulk download successful.")
    return file


@router.delete(
    "/{id:int}/delete",
    summary="⚠️ Delete a challenge",
    description="Delete a challenge with the specified ID. Requires admin privileges and password confirmation for security.",
    response_description="Confirmation of successful deletion",
)
async def delete_challenge_route_admin(
    id: Annotated[int, Path(title="The ID of the item to delete", ge=1)],
    current_active_user: Annotated[UserInDB, Depends(validate_active_user_password_dependency)],
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
) -> dict:
    """
    Delete challenge from database.
    The ID of entity to be deleted is taken from the URI.
    """
    logger.info(f"Received admin request to delete challenge with id {id} by {current_active_user.email}")
    await service.delete(id=id)
    logger.info(f"Challenge with id {id} deleted successfully by {current_active_user.email}.")
    return {"detail": "Challenge deleted"}


@router.delete(
    "/bulk-delete",
    response_model=BulkOperationResponse[Any],
    summary="⚠️ Delete multiple challenges",
    description="Delete multiple challenges with the specified IDs. Requires admin privileges and password confirmation for security.",
    response_description="Confirmation of successful deletion",
)
async def bulk_delete_challenges_route_admin(
    ids: Annotated[
        List[int],
        Body(..., description="List of challenge IDs to be deleted.", example=[1, 2, 3]),
    ],
    current_active_user: Annotated[UserInDB, Depends(validate_active_user_password_dependency)],
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
) -> BulkOperationResponse[Any]:
    """
    Delete multiple challenges from database with admin rights.
    The IDs of challenges to be deleted must be provided as a list.
    """
    logger.info(f"Received admin request to bulk delete {len(ids)} challenges  by {current_active_user.email}.")
    result = await service.delete_bulk(ids=ids)
    logger.info(result.detail, "Bulk delete successful.")
    return result


@router.delete(
    "/{id:int}/prune",
    response_model=BulkOperationResponse[Any],
    summary="☢️ Prune a challenge, its tasks and all histories ☢️",
    description="Delete a challenge, challenge histories, its related tasks and task histories. Requires admin privileges and password confirmation for security.",
    response_description="Confirmation of successful deletion",
)
async def prune_challenge_route_admin(
    id: Annotated[int, Path(title="The ID of the item to prune", ge=1)],
    current_active_user: Annotated[UserInDB, Depends(validate_active_user_password_dependency)],
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
) -> BulkOperationResponse[Any]:
    """
    Prune challenge from database: Delete the challenge, challenge histories, its related tasks and task histories.
    The ID of entity to be deleted is taken from the URI.
    """
    logger.info(f"Received admin request to prune challenge with id {id} by {current_active_user.email}")
    result = await service.prune_challenge(id=id)
    logger.info(f"Challenge with id {id} pruned successfully by {current_active_user.email}.")
    return result

@router.delete(
    "/bulk-prune",
    response_model=BulkOperationResponse[Any],
    summary="☢️ Prune multiple challenges, their tasks and all histories! ☢️",
    description="Prune multiple challenges with the specified IDs. Requires admin privileges and password confirmation for security.",
    response_description="Confirmation of successful deletion",
)
async def bulk_prune_challenges_route_admin(
    ids: Annotated[
        List[int],
        Body(..., description="List of challenge IDs to be pruned.", example=[1, 2, 3]),
    ],
    current_active_user: Annotated[UserInDB, Depends(validate_active_user_password_dependency)],
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
) -> BulkOperationResponse[Any]:
    """
    Prune multiple challenges from database with admin rights.
    Delete the challenges, challenge histories, their related tasks and task histories.
    The IDs of challenges to be deleted must be provided as a list.
    """
    logger.info(f"Received admin request to bulk delete {len(ids)} challenges  by {current_active_user.email}.")
    result = await service.prune_challenges_bulk(ids=ids)
    logger.info(result.detail, "Bulk prune successful.")
    return result


@router.get(
    "/{id:int}/histories",
    response_model=PaginationResponse,
    dependencies=[Depends(RoleChecker([Roles.ADMIN]))],
    summary="Get histories of challenge between status of DRAFT_SUBMITTED, REVISION_SUBMITTED, ACCEPT",
)
async def get_challenge_history_admin(
    id: int,
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
) -> PaginationResponse[Optional[List[ChallengeHistoryModelDTO]]]:
    logger.info(f"Received admin request to get histories of challenge with id {id} by {current_active_user.email}")

    entities, total_pages, total_records = await service.challenge_histories(id=id)
    logger.info("Challenge histories fetched successfully.")
    return PaginationResponse(
        total_pages=total_pages,
        total_records=total_records,
        content=entities,
    )


@router.delete(
    "/{id:int}/delete_history",
    summary="⚠️ Delete a challenge history",
    description="Delete a challenge history with the specified ID. Requires admin privileges and password confirmation for security.",
    response_description="Confirmation of successful deletion",
)
async def delete_challenge_history_route_admin(
    id: Annotated[int, Path(title="The ID of the item to delete", ge=1)],
    current_active_user: Annotated[UserInDB, Depends(validate_active_user_password_dependency)],
    service: Annotated[ChallengeService, Depends(get_challenge_service_admin)],
) -> dict:
    """
    Delete challenge history from database.
    The ID of entity to be deleted is taken from the URI.
    """
    logger.info(f"Received admin request to delete challenge history with id {id} by {current_active_user.email}")
    await service.challenge_history_service.delete(id=id)
    logger.info(f"Challenge history with id {id} deleted successfully by {current_active_user.email}.")
    return {"detail": "Challenge history deleted"}
