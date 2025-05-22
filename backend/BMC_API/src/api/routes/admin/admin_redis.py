# backend/BMC_API/src/api/routes/admin/admin_redis.py

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from redis.asyncio import ConnectionPool, Redis

from BMC_API.src.api.schemas.redis_schema import RedisValueDTO
from BMC_API.src.api.schemas.user_schema import UserInDB
from BMC_API.src.application.interfaces.authentication import (
    validate_active_user_password_dependency,
)
from BMC_API.src.application.interfaces.authorization import RoleChecker
from BMC_API.src.domain.value_objects.enums.user_enums import Roles
from BMC_API.src.infrastructure.external_services.redis.dependency import get_redis_pool

router = APIRouter(
    dependencies=[Depends(RoleChecker([Roles.ADMIN]))]
)  # IMPORTANT: dependency injection among all endpoints here for role checking

@router.get("/health")
async def redis_health(
    redis_pool: Annotated[ConnectionPool, Depends(get_redis_pool)],
) -> None:
    """
    Checks the health of a Redis server.
    """
    async with Redis(connection_pool=redis_pool) as redis:
        try:
            await redis.ping()
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    return {"message": "Redis server works"}

@router.get(
    "/",
    response_model=RedisValueDTO,
    summary="Get redis value (Admin)",
)
async def get_redis_value(
    key: str,
    redis_pool: Annotated[ConnectionPool, Depends(get_redis_pool)],
) -> RedisValueDTO:
    """
    Get value from redis.
    """
    async with Redis(connection_pool=redis_pool) as redis:
        try:
            redis_value = await redis.get(key)
            if not redis_value:
                raise
            else:
                return RedisValueDTO(
                    key=key,
                    value=redis_value,
                )
        except Exception as e:
            if 'No active exception' in str(e):
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Key not found.")
            else: 
                raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE )


@router.get(
    "/all_keys",
    response_model=List[RedisValueDTO],
    summary="Get all redis values (Admin)",
)
async def get_all_redis_values(
    redis_pool: Annotated[ConnectionPool, Depends(get_redis_pool)],
) -> RedisValueDTO:
    """
    Get all values from redis. Requires admin access.
    """
    async with Redis(connection_pool=redis_pool) as redis:
        try:
            keys = await redis.keys("*")

            if not keys:
                raise
            else:
                values = await redis.mget(keys)
                # results = list(zip(keys, values))
                results = []

                # convert keys and values to strings
                for key, value in zip(keys, values):
                    key_str = key.decode("utf-8", errors="ignore")
                    value_str = (
                        value.decode("utf-8", errors="ignore")
                        if value is not None
                        else None
                    )
                    results.append(
                        RedisValueDTO(
                            key=key_str,
                            value=value_str,
                        )
                    )
                return results
          
        except Exception as e:
            if 'No active exception' in str(e):
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No data found.")
            else: 
                raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                  )


@router.post(
    "/",
    summary="Set a redis values (Admin)",
)
async def set_redis_value(
    redis_value: RedisValueDTO,
    redis_pool: Annotated[ConnectionPool, Depends(get_redis_pool)],
) -> None:
    """
    Set value in redis.
    """
    if redis_value.value is not None:
        async with Redis(connection_pool=redis_pool) as redis:
            try:
                await redis.set(name=redis_value.key, value=redis_value.value)
            except Exception as e:
                logger.error(e)
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        return {"message": "key-value pair successfully stored in Redis database."}


@router.delete(
    "/",
    summary="Delete a key from Redis server (Admin)",
)
async def delete_redis_key(
    key: str,
    redis_pool: Annotated[ConnectionPool, Depends(get_redis_pool)],
) -> None:
    """
    Delete key&value pair from redis. 
    """

    async with Redis(connection_pool=redis_pool) as redis:
        try:
            redis_value = await redis.get(key)
            if not redis_value:
                raise
        except Exception as e:
            if 'No active exception' in str(e):
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Key not found.")
            else: 
                HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        try:
            await redis.delete(key)
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        return {"message": "key-value pair successfully deleted from Redis database."}


@router.delete(
    "/delete_all_keys",
    summary="Delete all keys from Redis server (Admin)",
)
async def delete_all_redis_keys(
    current_active_user: Annotated[UserInDB, Depends(validate_active_user_password_dependency)],
    redis_pool: Annotated[ConnectionPool, Depends(get_redis_pool)],
) -> None:
    """
    Delete ALL key&value pair from redis. Requires admin access and password validation.
    """
    try:
        async with Redis(connection_pool=redis_pool) as redis:
            keys = await redis.keys("*")
            await redis.delete(*keys)
    except Exception as e:
        logger.error(e)
        if 'No active exception' in str(e):
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Key not found.")
        else: 
            raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE )
    return {"message": "All key-value pairs successfully deleted from Redis database."}
