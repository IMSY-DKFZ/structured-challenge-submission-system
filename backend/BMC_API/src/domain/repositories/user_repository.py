# backend/BMC_API/src/domain/repositories/user_repository.py
from typing import Optional, Protocol

from BMC_API.src.domain.entities.user_model import UserModel
from BMC_API.src.domain.repositories.base_repository import (
    BaseRepositoryProtocol,
    TInput,
)


class UserRepositoryProtocol(BaseRepositoryProtocol[TInput, UserModel], Protocol):
    async def get_by_email(self, email: str) -> Optional[UserModel]: ...
    async def confirm_email(self, confirmation_token: str) -> None: ...
    async def reset_password(self, reset_token: str, new_password: str) -> None: ...
    async def login(self, email: str) -> Optional[UserModel]: ...
