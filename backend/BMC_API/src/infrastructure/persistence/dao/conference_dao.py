from typing import Tuple

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from BMC_API.src.domain.entities.conference_model import ConferenceModel
from BMC_API.src.infrastructure.persistence.dao.base_dao import BaseDAO


class SQLAlchemyConferenceRepository(BaseDAO[ConferenceModel]):
    """Class for accessing conference table."""

    # Set the model attribute so BaseDAO functions know which model to use.
    model = ConferenceModel

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        logger.debug(
            "SQLAlchemyconferenceRepository initialized for model: {}",
            self.model.__name__,
        )

    # async def pre_create_hook(self, obj: ConferenceModel) -> None:
    #     setattr(obj, "created_time", datetime.now())

    # async def pre_update_hook(self, entity: ConferenceModel) -> None:
    #     setattr(entity, "modified_time", datetime.now())

    async def list_conferences_of_user(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> Tuple[ConferenceModel, int, int]:
        """
        Get all conference models of the desired user with limit/offset pagination.

        :param limit: limit of conferences.
        :param offset: offset of conferences.
        :return: stream of conferences.
        """
        search_filters = {"owner_id": user_id}

        return super().list(limit=limit, offset=offset, search_filters=search_filters)
