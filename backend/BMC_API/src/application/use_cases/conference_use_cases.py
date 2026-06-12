# application/use_cases/conference_use_cases.py

from datetime import datetime
from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel, ValidationError

from BMC_API.src.api.dependencies.schemas import BulkOperationResponse
from BMC_API.src.application.dto.conference_dto import (
    ConferenceModelBaseOutputDTO,
    ConferenceResponseAdminDTO,
    ConferenceUpdateAdminDTO,
)
from BMC_API.src.application.use_cases.base_use_cases import BaseService
from BMC_API.src.core.validation_errors import format_validation_error
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

    async def update_bulk(self, updates: List[Dict[str, Any]]) -> BulkOperationResponse[ConferenceResponseAdminDTO]:
        prepared_updates = []
        failed_results = []
        for entity_data in updates:
            if "id" not in entity_data:
                prepared_updates.append(entity_data)
                continue

            entity_id = entity_data["id"]
            update_data = {key: value for key, value in entity_data.items() if key != "id"}
            try:
                validated_data = ConferenceUpdateAdminDTO.model_validate(update_data).model_dump(exclude_unset=True)
            except ValidationError as e:
                failed_results.append({"data": entity_data, "error": format_validation_error(e)})
                continue

            prepared_updates.append({"id": entity_id, **validated_data, "modified_time": datetime.now()})

        result = await super().update_bulk(updates=prepared_updates)
        result.failed.extend(failed_results)
        result.detail = f"Bulk update completed: {len(result.successful)} successful, {len(result.failed)} failed."
        return result
