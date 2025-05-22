# backend/BMC_API/src/api/routes/user.py
# Exceptions raised the routes here will be caught by the global exception handlers.

from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from loguru import logger

from BMC_API.src.api.dependencies.route_dependencies import get_repository, get_service
from BMC_API.src.api.dependencies.schemas import PaginationResponse
from BMC_API.src.application.dto.conference_dto import ConferenceModelBaseOutputDTO
from BMC_API.src.application.use_cases.conference_use_cases import ConferenceService
from BMC_API.src.infrastructure.persistence.dao.conference_dao import (
    SQLAlchemyConferenceRepository,
)

router = APIRouter()


# Dependency functions
repository_dependency = get_repository(SQLAlchemyConferenceRepository)
service_dependency = get_service(ConferenceService, repository_dependency, dto_class=ConferenceModelBaseOutputDTO)


@router.get("/all_limited", response_model=PaginationResponse)
async def get_all_conferences_limited_route(
    service: Annotated[ConferenceService, Depends(service_dependency)],
) -> PaginationResponse[Optional[ConferenceModelBaseOutputDTO]]:
    logger.info("Received request to get all conferences open for submission")
    (
        entities,
        total_pages,
        total_records,
    ) = await service.list_conferences_open_for_submission_limited(offset=0, limit=0)

    if not entities:
        logger.info("No conference found")
    else:
        logger.info("Conferences retrieved")
    return PaginationResponse(
        total_pages=total_pages,
        total_records=total_records,
        content=entities,
    )
