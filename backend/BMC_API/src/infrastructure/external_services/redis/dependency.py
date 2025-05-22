# backend/BMC_API/src/infrastructure/external_services/redis/dependency.py
from typing import AsyncGenerator

from fastapi import Depends
from starlette.requests import Request

from BMC_API.src.infrastructure.external_services.redis.token_cache_impl import (
    RedisTokenCache,
)
from redis.asyncio import ConnectionPool, Redis


async def get_redis_pool(
    request: Request,
) -> AsyncGenerator[Redis, None]:  # pragma: no cover
    """
    Returns connection pool.

    You can use it like this:

    >>> from redis.asyncio import ConnectionPool, Redis
    >>>
    >>> async def handler(redis_pool: ConnectionPool = Depends(get_redis_pool)):
    >>>     async with Redis(connection_pool=redis_pool) as redis:
    >>>         await redis.get('key')

    I use pools, so you don't acquire connection till the end of the handler.

    :param request: current request.
    :returns:  redis connection pool.
    """
    return request.app.state.redis_pool


def get_token_cache(
    redis_pool: ConnectionPool = Depends(get_redis_pool),
) -> RedisTokenCache:
    """
    Returns an instance of RedisTokenCache which implements the TokenCache interface.
    """
    return RedisTokenCache(redis_pool)
