# backend/BMC_API/src/infrastructure/external_services/redis/token_cache_impl.py
from datetime import timedelta

from BMC_API.src.domain.interfaces.token_cache import TokenCache
from redis.asyncio import ConnectionPool, Redis


class RedisTokenCache(TokenCache):
    def __init__(self, redis_pool: ConnectionPool):
        self.redis = Redis(connection_pool=redis_pool)

    async def set_token(self, key: str, value: str, expire: timedelta) -> None:
        await self.redis.set(name=key, value=value, ex=expire)

    async def get_token(self, key: str) -> str | None:
        return await self.redis.get(name=key)

    async def delete_token(self, key: str) -> None:
        await self.redis.delete(name=key)
