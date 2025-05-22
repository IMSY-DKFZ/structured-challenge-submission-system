# application/use_cases/conference_use_cases.py

from typing import Optional, Type

from pydantic import BaseModel

from BMC_API.src.application.dto.conference_dto import (
    ConferenceModelBaseOutputDTO,
    ConferenceResponseAdminDTO,
)
from BMC_API.src.application.use_cases.base_use_cases import BaseService
from BMC_API.src.domain.entities.conference_model import ConferenceModel
from BMC_API.src.domain.interfaces.token_cache import TokenCache
from BMC_API.src.domain.repositories.conference_repository import (
    ConferenceRepositoryProtocol,
)


class ConferenceService(BaseService[ConferenceModel, ConferenceModelBaseOutputDTO]):
    def __init__(
        self,
        repository: ConferenceRepositoryProtocol,
        dto_class: Optional[Type[BaseModel]] = None,
        token_cache: Optional[TokenCache] = None,
    ) -> None:
        super().__init__(repository, dto_class)
        self.token_cache = token_cache

    async def list_conferences_open_for_submission_limited(
        self, offset: int = 0, limit: int = 50
    ) -> Optional[ConferenceModelBaseOutputDTO]:
        search_filters = {"is_open_for_submissions": True}
        return await super().list(offset=offset, limit=limit, search_filters=search_filters)

    async def list_conferences_of_user(
        self, user_id: int, offset: int = 0, limit: int = 50
    ) -> Optional[ConferenceResponseAdminDTO]:
        search_filters = {"owner_id": user_id}
        return await super().list(offset=offset, limit=limit, search_filters=search_filters)
