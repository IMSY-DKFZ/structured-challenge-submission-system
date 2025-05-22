# backend/BMC_API/src/api/routes/admin_conference.py
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

# from pydantic import EmailStr
from BMC_API.src.api.schemas.user_schema import UserInDB
from BMC_API.src.application.dto.conference_dto import (
    ConferenceCreateAdminDTO,
    ConferenceResponseAdminDTO,
    ConferenceUpdateAdminDTO,
)
from BMC_API.src.application.interfaces.authentication import (
    ensure_current_active_user,
    validate_active_user_password_dependency,
)
from BMC_API.src.application.interfaces.authorization import RoleChecker
from BMC_API.src.application.use_cases.conference_use_cases import ConferenceService

# from BMC_API.src.application.use_cases.user_use_cases import UserService
from BMC_API.src.domain.value_objects.enums.user_enums import Roles
from BMC_API.src.infrastructure.persistence.dao.conference_dao import (
    SQLAlchemyConferenceRepository,
)

router = APIRouter(
    dependencies=[Depends(RoleChecker([Roles.ADMIN]))]
)  # IMPORTANT: dependency injection among all endpoints here for role checking


# Dependency functions
repository_dependency = get_repository(SQLAlchemyConferenceRepository)
service_dependency = get_service(ConferenceService, repository_dependency, dto_class=ConferenceResponseAdminDTO)


# Admin routes for conference management
@router.get("/{id:int}", response_model=Optional[ConferenceResponseAdminDTO])
async def get_conference_route_admin(
    id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
    service: Annotated[ConferenceService, Depends(service_dependency)],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
) -> Optional[ConferenceResponseAdminDTO]:
    """
    Retrieve a conference by its ID.

    This endpoint fetches the details of a conference identified by its unique ID.
    If the conference exists, it returns the conference data as a ConferenceResponseAdminDTO.
    If not found, it returns None.

    **Parameters:**

    * `id (int)`: The unique identifier of the conference to retrieve. Must be a positive integer.

    **Returns:**

    * `Optional[ConferenceResponseAdminDTO]`: The conference details if found; otherwise, None.
    """
    logger.info(f"Received admin request to get conference with id {id} by {current_active_user.email}")
    entity: ConferenceResponseAdminDTO = await service.get(id=id)
    logger.info(f"Conference with id {id} retrieved  by {current_active_user.email}")
    return entity


@router.post("/all", response_model=PaginationResponse, response_model_exclude_none=True)
async def list_conferences_route_admin(
    service: Annotated[ConferenceService, Depends(service_dependency)],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    limit: int | None = None,
    offset: int | None = None,
    search_request: SearchRequest | None = None,
    sort_by: str | None = "id",
    sort_desc: bool | None = False,
) -> PaginationResponse:
    """
    Retrieve a paginated list of conferences for admin users.

    This endpoint allows an admin user to fetch a list of conferences with support for pagination,
    optional filtering, and sorting. The search_request may include search filters and output filters
    to refine the query. The response is structured as a PaginationResponse containing the list of
    conference entities along with metadata such as total pages and total records.

    **Parameters:**

    * `limit (Optional[int])`: Maximum number of records to return. Defaults to None.

    * `offset (Optional[int])`: The starting index for the records to return. Defaults to None.

    * `search_request (Optional[SearchRequest])`: An object that may contain:
        * `search_filters`: Conditions for filtering the conference records.

        * `output_filters`: Fields to include in the response.
    * `sort_by (Optional[str])`: The field name to sort the results by (default is "id").

    * `sort_desc (Optional[bool])`: Determines if sorting should be in descending order (default is False).

    **Returns:**

    * `PaginationResponse`: A response object containing:

        * `total_pages`: Total number of pages available.

        * `total_records`: Total number of conference records matching the query.

        * `content`: A list of conference entities for the current page.
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


@router.post(
    "/create",
    response_model=ConferenceResponseAdminDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_conference_route_admin(
    model_create: Annotated[
        ConferenceCreateAdminDTO,
        Body(
            ...,
            description="Conference creation details.",
        ),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[ConferenceService, Depends(service_dependency)],
) -> ConferenceResponseAdminDTO:
    """
    Create a new conference.
    """
    logger.info(f"Received admin request to create conference by {current_active_user.email}")
    entity_data = model_create.model_dump()
    entity_data["owner_id"] = current_active_user.id
    entity_data["created_time"] = datetime.now()

    created = await service.create(model_create=entity_data)
    logger.info(f"Conference {created.id} created successfully by {current_active_user.email}.")
    return created


@router.put(
    "/{id:int}/update",
    response_model=ConferenceResponseAdminDTO,
    response_model_exclude_none=True,
)
async def update_conference_route_admin(
    id: Annotated[int, Path(title="The ID of the item to update", ge=1)],
    model_update: Annotated[
        ConferenceUpdateAdminDTO,
        Body(..., description="The updated conference details."),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[ConferenceService, Depends(service_dependency)],
) -> ConferenceResponseAdminDTO:
    """
    Update an existing conference's details with admin rights. The conference ID is taken from the URI.
    """
    logger.info(f"Received admin request to update conference with id {id}  by {current_active_user.email}")

    entity_data = model_update.model_dump()
    entity_data["modified_time"] = datetime.now()

    updated = await service.update(id=id, model_update=entity_data)
    logger.info(f"Conference with id {updated.id} updated successfully by {current_active_user.email}.")
    return updated


@router.put("/bulk-update", response_model=BulkOperationResponse[ConferenceResponseAdminDTO])
async def bulk_update_conferences_route_admin(
    updates: Annotated[
        List[Dict[str, Any]],
        Body(
            examples=[[{"id": 1, "field": "string"}, {"id": 2, "field": "string"}]],
            title="The updated conference details.",
            description="List of conference updates. Each item should contain 'id' and update data (column names as keys and values).",
        ),
    ],
    current_active_user: Annotated[UserInDB, Depends(ensure_current_active_user)],
    service: Annotated[ConferenceService, Depends(service_dependency)],
) -> BulkOperationResponse[ConferenceResponseAdminDTO]:
    """
    Bulk update multiple conferences' details with admin rights.
    Each update in the list must contain the conference ID and the fields to update.
    """
    logger.info(f"Received admin request to bulk update {len(updates)} conferences  by {current_active_user.email}.")
    [entity_data.update({"modified_time": datetime.now()}) for entity_data in updates]
    result = await service.update_bulk(updates=updates)
    logger.info(result.detail, "Bulk updates successful.")
    return result


@router.delete(
    "/{id:int}/delete",
    summary="⚠️ Delete a conference",
    description="Delete a conference with the specified ID. Requires admin privileges and password confirmation for security.",
    response_description="Confirmation of successful deletion",
)
async def delete_conference_route_admin(
    id: Annotated[int, Path(title="The ID of the item to delete", ge=1)],
    current_active_user: Annotated[UserInDB, Depends(validate_active_user_password_dependency)],
    service: Annotated[ConferenceService, Depends(service_dependency)],
) -> dict:
    """
    Delete conference from database with admin rights.
    The ID of conference to be deleted is taken from the URI.
    """
    logger.info(f"Received admin request to delete conference with id {id}  by {current_active_user.email}")
    await service.delete(id=id)
    logger.info(f"Conference with id: {id} deleted successfully by {current_active_user.email}.")
    return {"detail": "Conference deleted"}


@router.delete(
    "/bulk-delete",
    response_model=BulkOperationResponse[Any],
    summary="⚠️ Delete multiple conferences",
    description="Delete multiple conferences with the specified IDs. Requires admin privileges and password confirmation for security.",
    response_description="Confirmation of successful deletion",
)
async def bulk_delete_conferences_route_admin(
    ids: Annotated[
        List[int],
        Body(..., description="List of conference IDs to be deleted.", example=[1, 2, 3]),
    ],
    current_active_user: Annotated[UserInDB, Depends(validate_active_user_password_dependency)],
    service: Annotated[ConferenceService, Depends(service_dependency)],
) -> BulkOperationResponse[Any]:
    """
    Delete multiple conferences from database with admin rights.
    The IDs of conferences to be deleted must be provided as a list.
    """
    logger.info(f"Received admin request to bulk delete {len(ids)} conferences  by {current_active_user.email}.")
    result = await service.delete_bulk(ids=ids)
    logger.info(result.detail, "Bulk delete successful.")
    return result
