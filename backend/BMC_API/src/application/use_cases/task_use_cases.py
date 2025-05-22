# application/use_cases/task_use_cases.py


from datetime import datetime
from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel, TypeAdapter

from BMC_API.src.api.dependencies.schemas import BulkOperationResponse
from BMC_API.src.application.dto.task_dto import (
    TaskHistoryModelDTO,
    TaskModelBaseOutputDTO,
)
from BMC_API.src.application.use_cases.base_use_cases import BaseService
from BMC_API.src.core.exceptions import RepositoryException
from BMC_API.src.domain.entities.task_model import TaskModel
from BMC_API.src.domain.interfaces.token_cache import TokenCache
from BMC_API.src.domain.repositories.task_repository import TaskRepositoryProtocol
from BMC_API.src.domain.services.status_manager import StatusActions


class TaskService(BaseService[TaskModel, TaskModelBaseOutputDTO]):
    def __init__(
        self,
        repository: TaskRepositoryProtocol,
        dto_class: Optional[Type[BaseModel]] = None,
        token_cache: Optional[TokenCache] = None,
    ) -> None:
        super().__init__(repository, dto_class)
        self.token_cache = token_cache

    async def task_histories(self, id: int) -> List:
        obj = await super().get_raw(id)
        if obj.histories:
            return (
                TypeAdapter(List[TaskHistoryModelDTO]).validate_python(obj.histories),
                1,
                len(obj.histories),
            )
        else:
            raise RepositoryException(f"No history found for task {id}")

    async def update_task(self, id: int, model_update: Dict) -> TaskModelBaseOutputDTO:
        # New status class here
        task_obj = await self.get_raw(id)
        current_status = task_obj.task_status
        new_status = StatusActions.next_status_for_update(current_status)
        model_update["task_modified_time"] = datetime.now()
        model_update["task_status"] = new_status
        return await super().update(id=id, model_update=model_update)

    async def update_task_bulk(self, updates: List[Dict[str, Any]]) -> BulkOperationResponse[TaskModelBaseOutputDTO]:
        for entity_data in updates:
            task_obj = await self.get_raw(entity_data["id"])
            current_status = task_obj.task_status
            new_status = StatusActions.next_status_for_update(current_status)
            entity_data["task_modified_time"] = datetime.now()
            entity_data["task_status"] = new_status

        return await super().update_bulk(updates=updates)
