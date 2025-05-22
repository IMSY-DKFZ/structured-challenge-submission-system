# backend/BMC_API/src/infrastructure/persistence/dao/challenge_history_dao.py

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from BMC_API.src.domain.entities.challenge_history_model import ChallengeHistoryModel
from BMC_API.src.infrastructure.persistence.dao.base_dao import BaseDAO


class SQLAlchemyChallengeHistoryRepository(BaseDAO[ChallengeHistoryModel]):
    """Class for accessing challenge table."""

    # Set the model attribute so BaseDAO functions know which model to use.
    model = ChallengeHistoryModel

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        logger.debug(
            "SQLAlchemyChallengeHistoryRepository initialized for model: {}",
            self.model.__name__,
        )
