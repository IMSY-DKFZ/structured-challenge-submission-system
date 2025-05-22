# backend/BMC_API/src/domain/repositories/task_history_repository.py
from typing import Protocol

from BMC_API.src.domain.entities.task_history_model import TaskHistoryModel
from BMC_API.src.domain.repositories.base_repository import (
    BaseRepositoryProtocol,
    TInput,
)


class TaskHistoryRepositoryProtocol(BaseRepositoryProtocol[TInput, TaskHistoryModel], Protocol):
    pass
