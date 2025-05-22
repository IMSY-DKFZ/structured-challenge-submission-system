# backend/BMC_API/src/domain/repositories/challenge_history_repository.py
from typing import Protocol

from BMC_API.src.domain.entities.challenge_history_model import ChallengeHistoryModel
from BMC_API.src.domain.repositories.base_repository import (
    BaseRepositoryProtocol,
    TInput,
)


class ChallengeHistoryRepositoryProtocol(BaseRepositoryProtocol[TInput, ChallengeHistoryModel], Protocol):
    pass
