# application/use_cases/task_history_use_cases.py


from typing import Optional, Type

from pydantic import BaseModel

from BMC_API.src.application.dto.task_dto import TaskHistoryModelDTO
from BMC_API.src.application.use_cases.base_use_cases import BaseService
from BMC_API.src.domain.entities.task_history_model import TaskHistoryModel
from BMC_API.src.domain.interfaces.token_cache import TokenCache
from BMC_API.src.domain.repositories.task_history_repository import (
    TaskHistoryRepositoryProtocol,
)


class TaskHistoryService(BaseService[TaskHistoryModel, TaskHistoryModelDTO]):
    def __init__(
        self,
        repository: TaskHistoryRepositoryProtocol,
        dto_class: Optional[Type[BaseModel]] = None,
        token_cache: Optional[TokenCache] = None,
    ) -> None:
        super().__init__(repository, dto_class)
        self.token_cache = token_cache
