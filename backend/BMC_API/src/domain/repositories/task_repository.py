# backend/BMC_API/src/domain/repositories/task_repository.py
from typing import Optional, Protocol

from BMC_API.src.domain.entities.task_model import TaskModel
from BMC_API.src.domain.repositories.base_repository import (
    BaseRepositoryProtocol,
    TInput,
)


class TaskRepositoryProtocol(BaseRepositoryProtocol[TInput, TaskModel], Protocol):
    async def list_tasks_of_user(self, user_id: int, offset: int = 0, limit: int = 50) -> Optional[TaskModel]: ...
