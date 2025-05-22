# backend/BMC_API/src/initial_data.py
# ruff: noqa: E402
from datetime import datetime

import bcrypt
from fastapi import FastAPI
from sqlalchemy import select

from BMC_API.src.core.config.settings import settings
from BMC_API.src.domain.entities.user_model import UserModel
from BMC_API.src.domain.value_objects.enums.user_enums import Roles


async def _create_initial_admin(app: FastAPI) -> None:
    """Creates the initial admin account in the database."""
    async with app.state.db_session_factory() as session:
        query = select(UserModel)
        query = query.where(UserModel.email == settings.DEFAULT_ADMIN_NAME)

        rows = await session.execute(query)
        user = rows.scalars().first()
        if not user:
            new_user_dict = {}
            new_user_dict["email"] = settings.DEFAULT_ADMIN_NAME
            password = settings.DEFAULT_ADMIN_PASSWORD.encode("utf-8")
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(10))
            new_user_dict["password"] = hashed_password
            new_user_dict["first_name"] = "Initial"
            new_user_dict["last_name"] = "Admin"
            new_user_dict["created_time"] = datetime.now()
            new_user_dict["roles"] = [Roles.ADMIN]
            new_user_dict["email_confirmed"] = True

            new_user = UserModel(**new_user_dict)
            session.add(new_user)
            await session.commit()
            await session.close()




async def create_initial_data(app: FastAPI) -> None:
    await _create_initial_admin(app)

