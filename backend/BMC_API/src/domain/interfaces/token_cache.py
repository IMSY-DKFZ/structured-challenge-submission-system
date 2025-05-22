# backend/BMC_API/src/domain/interfaces/token_cache.py
from datetime import timedelta
from typing import Protocol


class TokenCache(Protocol):
    async def set_token(self, key: str, value: str, expire: timedelta) -> None: ...

    async def get_token(self, key: str) -> str | None: ...

    async def delete_token(self, key: str) -> None: ...
