# backend/BMC_API/src/infrastructure/persistence/dao/challenge_dao.py

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from BMC_API.src.domain.entities.challenge_model import ChallengeModel
from BMC_API.src.infrastructure.persistence.dao.base_dao import BaseDAO


class SQLAlchemyChallengeRepository(BaseDAO[ChallengeModel]):
    """Class for accessing challenge table."""

    # Set the model attribute so BaseDAO functions know which model to use.
    model = ChallengeModel

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        logger.debug(
            "SQLAlchemyChallengeRepository initialized for model: {}",
            self.model.__name__,
        )
