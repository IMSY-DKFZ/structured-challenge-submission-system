# backend/BMC_API/src/domain/repositories/challenge_repository.py
from typing import Any, Dict, List, Protocol

from fastapi import BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse

from BMC_API.src.api.dependencies.schemas import BulkOperationResponse
from BMC_API.src.application.dto.challenge_dto import (
    ChallengeHistoryModelDTO,
    ChallengeModelBaseOutputDTO,
)
from BMC_API.src.application.use_cases.task_use_cases import TaskService
from BMC_API.src.domain.entities.challenge_model import ChallengeModel
from BMC_API.src.domain.repositories.base_repository import (
    BaseRepositoryProtocol,
    TInput,
)
from BMC_API.src.domain.value_objects.enums.challenge_enums import ChallengeStatus


class ChallengeRepositoryProtocol(BaseRepositoryProtocol[TInput, ChallengeModel], Protocol):
    async def challenge_histories(self, id: int) -> List[ChallengeHistoryModelDTO]: ...
    async def update_challenge(self, id: int, model_update: Dict) -> ChallengeModelBaseOutputDTO: ...
    async def update_challenge_bulk(
        self, updates: List[Dict[str, Any]]
    ) -> BulkOperationResponse[ChallengeModelBaseOutputDTO]: ...
    async def prune_challenge(self, id: int) -> BulkOperationResponse: ...
    async def download_challenge(self, id: int) -> FileResponse: ...
    async def download_challenge_bulk(self, ids: List[int]) -> StreamingResponse: ...
    async def status(
        self, id: int, new_status: ChallengeStatus, task_service: TaskService
    ) -> ChallengeModelBaseOutputDTO: ...
    async def bulk_status(
        self, ids: List[int], new_status: str
    ) -> BulkOperationResponse[ChallengeModelBaseOutputDTO]: ...
    async def take_snapshot(self, id: int): ...
    async def submit_challenge(
        self, id: int, background_tasks: BackgroundTasks, send_notification_emails: bool
    ) -> None: ...
