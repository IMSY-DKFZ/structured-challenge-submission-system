# backend/BMC_API/src/infrastructure/persistence/dao/task_dao.py

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from BMC_API.src.domain.entities.task_model import TaskModel
from BMC_API.src.infrastructure.persistence.dao.base_dao import BaseDAO


class SQLAlchemyTaskRepository(BaseDAO[TaskModel]):
    """Class for accessing task table."""

    # Set the model attribute so BaseDAO functions know which model to use.
    model = TaskModel

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        logger.debug(
            "SQLAlchemyTaskRepository initialized for model: {}",
            self.model.__name__,
        )

    # async def list_tasks_of_user(
    #     self,
    #     user_id: int,
    #     limit: int,
    #     offset: int,
    # ) -> Tuple[TaskModel, int, int]:
    #     """
    #     Get all task models of the desired user with limit/offset pagination.

    #     :param limit: limit of task.
    #     :param offset: offset of task.
    #     :return: stream of task.
    #     """
    #     search_filters = {"task_owner_id": user_id}

    #     return await super().list(limit=limit, offset=offset, search_filters=search_filters)
