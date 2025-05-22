# backend/BMC_API/src/infrastructure/persistence/dao/user_dao.py
from datetime import datetime
from typing import Optional

from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from BMC_API.src.core.exceptions import (
    RepositoryException,
)
from BMC_API.src.domain.entities.user_model import UserModel
from BMC_API.src.infrastructure.persistence.dao.base_dao import BaseDAO


class SQLAlchemyUserRepository(BaseDAO[UserModel]):
    # Set the model attribute so BaseDAO functions know which model to use.
    model = UserModel

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        logger.debug(
            "SQLAlchemyUserRepository initialized for model: {}", self.model.__name__
        )

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        logger.debug("Retrieving user by email: {}", email)
        query = select(self.model).where(self.model.email == email)
        result = await self.session.execute(query)
        user = result.scalars().first()
        if user:
            logger.debug("Found user: {}", user.email)
            return user
        logger.debug("User with email {} not found", email)
        return None

    async def confirm_email(self, confirmation_token: str) -> None:
        logger.debug("Confirming email with token: {}", confirmation_token)
        query = select(self.model).where(
            self.model.email_confirmation_token == confirmation_token
        )
        result = await self.session.execute(query)
        user = result.scalars().first()
        if not user:
            logger.error("Invalid confirmation token: {}", confirmation_token)
            raise RepositoryException("Invalid confirmation token.")
        if user.email_confirmed:
            logger.debug("Email already confirmed for user: {}", user.email)
            raise RepositoryException("Email already confirmed.")
        user.email_confirmed = True
        user.email_confirmation_token = None
        user.modified_time = datetime.now()

        try:
            await self.session.commit()
            logger.debug("User  confirmed: {}", user.email)
        except IntegrityError as e:
            await self.session.rollback()
            logger.error(
                "Error confirming email for token {}: {}", confirmation_token, e
            )
            raise RepositoryException("Error confirming email.") from e

    async def reset_password(self, reset_token: str, new_password: str) -> None:
        logger.debug("Resetting password using token: {}", reset_token)
        query = select(self.model).where(self.model.reset_token == reset_token)
        result = await self.session.execute(query)
        user = result.scalars().first()
        if not user:
            logger.error("Invalid reset token: {}", reset_token)
            raise RepositoryException("Invalid reset token.")
        user.password = new_password  # new_password is already hashed.
        user.reset_token = None
        user.modified_time = datetime.now()
        try:
            await self.session.commit()
            logger.debug("Password reset successfully for user: {}", user.email)
        except IntegrityError as e:
            await self.session.rollback()
            logger.error("Error resetting password for token {}: {}", reset_token, e)
            raise RepositoryException("Error resetting password.") from e

    async def login(self, email: str) -> None:
        logger.debug("Attempting login for user: {}", email)
        query = select(self.model).where(self.model.email == email)
        result = await self.session.execute(query)
        user = result.scalars().first()
        if not user:
            logger.warning("Login failed: user with email {} not found", email)
            return user

        try:
            user.last_login_time = datetime.now()
            await self.session.commit()
            await self.session.refresh(user)
            logger.debug("Login successful for user: {}", user.email)
        except IntegrityError as e:
            logger.error(
                "Error during logging user with ID: {}. Error: {e}", user.id, e
            )
            await self.session.rollback()
        except Exception as e:
            await self.session.rollback()
            logger.error(e)
