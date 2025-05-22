# application/use_cases/challenge_history_use_cases.py


from typing import Optional, Type

from pydantic import BaseModel

from BMC_API.src.application.dto.challenge_dto import ChallengeHistoryModelDTO
from BMC_API.src.application.use_cases.base_use_cases import BaseService
from BMC_API.src.domain.entities.challenge_history_model import ChallengeHistoryModel
from BMC_API.src.domain.interfaces.token_cache import TokenCache
from BMC_API.src.domain.repositories.challenge_history_repository import (
    ChallengeHistoryRepositoryProtocol,
)


class ChallengeHistoryService(BaseService[ChallengeHistoryModel, ChallengeHistoryModelDTO]):
    def __init__(
        self,
        repository: ChallengeHistoryRepositoryProtocol,
        dto_class: Optional[Type[BaseModel]] = None,
        token_cache: Optional[TokenCache] = None,
    ) -> None:
        super().__init__(repository, dto_class)
        self.token_cache = token_cache
