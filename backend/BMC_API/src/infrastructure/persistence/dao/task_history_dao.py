# backend/BMC_API/src/infrastructure/persistence/dao/task_history_dao.py

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from BMC_API.src.domain.entities.task_history_model import TaskHistoryModel
from BMC_API.src.infrastructure.persistence.dao.base_dao import BaseDAO


class SQLAlchemyTaskHistoryRepository(BaseDAO[TaskHistoryModel]):
    """Class for accessing challenge table."""

    # Set the model attribute so BaseDAO functions know which model to use.
    model = TaskHistoryModel

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        logger.debug(
            "SQLAlchemyTaskHistoryRepository initialized for model: {}",
            self.model.__name__,
        )
