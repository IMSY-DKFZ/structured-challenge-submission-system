# backend/BMC_API/src/api/routes/admin.py
# Exceptions raised the routes here will be caught by the global exception handlers.

import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger

from BMC_API.src.api.schemas.user_schema import UserInDB
from BMC_API.src.application.interfaces.authentication import (
    validate_active_user_password_dependency,
)
from BMC_API.src.application.interfaces.authorization import RoleChecker

# from BMC_API.src.application.use_cases.user_use_cases import UserService
from BMC_API.src.domain.value_objects.enums.user_enums import Roles
from BMC_API.src.infrastructure.persistence.dependencies import (
    backup_database,
    delete_db_backups,
)

router = APIRouter(
    dependencies=[Depends(RoleChecker([Roles.ADMIN]))]
)  # IMPORTANT: dependency injection among all endpoints here for role checking

@router.post(
    "/database_backup_and_download"
)
async def database_backup_and_download(file_name: str | None = None) -> FileResponse:
    try:
        backup_file_location = await backup_database(file_name)
        os.stat(backup_file_location)
        if not file_name:
            file_name = os.path.basename(backup_file_location)
        elif not file_name.endswith(".sqlite3"):
            file_name = f"{file_name}.sqlite3"
        else:
            file_name = f"{file_name}"

        return FileResponse(
            path=backup_file_location,
            media_type="application/octet-stream",
            filename=file_name,
        )
    except RuntimeError as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=503,
            detail="Something went wrong. Please contact the admins",
        )
    except FileNotFoundError as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=404,
            detail="Database file not found. Please contact the admins",
        )
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=503,
            detail="Something went wrong. Please contact the admins",
        )


@router.delete(
    "/delete_database_backups"
)
async def delete_database_backups(

    current_active_user: Annotated[UserInDB, Depends(validate_active_user_password_dependency)],
    delete_all_backups: bool = False,
) -> JSONResponse:

    try:
        deleted_files = await delete_db_backups(delete_all_backups)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=503,
            detail="Something went wrong. Please contact the admins",
        )

    # Return success message
    if not delete_all_backups:
        message = "All database backups except the latest one successfully deleted."
    else:
        message = "All database backups successfully deleted."

    return JSONResponse(
        status_code=200,
        content={"message": message, "deleted_files": deleted_files},
    )
