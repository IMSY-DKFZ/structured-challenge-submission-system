# backend/BMC_API/src/domain/repositories/conference_repository.py
from typing import Optional, Protocol

from BMC_API.src.domain.entities.conference_model import ConferenceModel
from BMC_API.src.domain.repositories.base_repository import (
    BaseRepositoryProtocol,
    TInput,
)


class ConferenceRepositoryProtocol(
    BaseRepositoryProtocol[TInput, ConferenceModel], Protocol
):
    async def list_conferences_of_user(
        self, user_id: int, offset: int = 0, limit: int = 50
    ) -> Optional[ConferenceModel]: ...
