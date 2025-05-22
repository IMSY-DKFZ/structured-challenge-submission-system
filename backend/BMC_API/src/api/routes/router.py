"""
This file is excluded from formatters(Ruff, Black). The oder of the imports
from BMC_API.src.api.routes should not be changed. Otherwise "circular import" error happens.
"""

from fastapi.routing import APIRouter

from BMC_API.src.api.routes import (  # redis_routes,
    challenge,
    conference,
    contact,
    echo,
    monitoring,
    task,
    user,
)
from BMC_API.src.api.routes.admin import (
    admin_challenge,
    admin_conference,
    admin_database,
    admin_redis,
    admin_task,
    admin_user,
)

api_router = APIRouter()
# api_router.include_router(redis_routes.router, prefix="/redis", tags=["redis"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(conference.router, prefix="/conference", tags=["Conference"])
api_router.include_router(challenge.router, prefix="/challenge", tags=["Challenge"])
api_router.include_router(task.router, prefix="/task", tags=["Task"])
api_router.include_router(monitoring.router, tags=["Health"])
api_router.include_router(echo.router, prefix="/echo", tags=["Echo"])
api_router.include_router(contact.router, prefix="/contact", tags=["Contact"])
api_router.include_router(admin_user.router, prefix="/admin/user", tags=["Admin (User routes)"])
api_router.include_router(
    admin_conference.router,
    prefix="/admin/conference",
    tags=["Admin (Conference routes)"],
)
api_router.include_router(
    admin_challenge.router,
    prefix="/admin/challenge",
    tags=["Admin (Challenge routes)"],
)
api_router.include_router(
    admin_task.router,
    prefix="/admin/task",
    tags=["Admin (Task routes)"],
)
api_router.include_router(
    admin_database.router,
    prefix="/admin/database",
    tags=["Admin (Database)"],
)
api_router.include_router(
    admin_redis.router,
    prefix="/admin/redis",
    tags=["Admin (Redis)"],
)
