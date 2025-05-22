# backend/BMC_API/src/infrastructure/persistence/dependencies.py
import glob
import os
import sqlite3
import time
from datetime import datetime
from typing import AsyncGenerator

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from starlette.requests import Request

from BMC_API.src.core.config.settings import settings


def create_db_session() -> AsyncSession:  # pragma: no cover
    """
    Creates new connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """
    engine = create_async_engine(str(settings.db_url), echo=settings.db_echo)
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

    session: AsyncSession = session_factory()
    return session


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_session_factory()

    try:  # noqa: WPS501
        yield session
    finally:
        await session.commit()
        await session.close()


async def backup_database(file_name: str | None = None):
    db_file = str(settings.db_file_abs)
    if os.path.exists(db_file):
        # Connect current database
        src = sqlite3.connect(db_file)

        # Arrange backup folder
        backup_folder = str(settings.backup_folder)
        if not os.path.exists(backup_folder):
            os.mkdir(backup_folder)

        # Create backup filename and location
        if file_name:
            backup_file_name = file_name + ".sqlite3"

        else:
            backup_file_name = (
                "database_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".sqlite3"
            )
        backup_file_location = os.path.join(backup_folder, backup_file_name)

        try:
            dst = sqlite3.connect(backup_file_location)  # Connect backup database
            src.backup(dst)  # Make backup
            logger.info(f"Database backup created: {backup_file_location}")

        except Exception as e:
            logger.error(e)
            raise

        return backup_file_location


async def delete_db_backups(delete_all_backups: bool = False) -> list:
    # Get the backup folder path
    backup_folder = str(settings.backup_folder)

    # Check if the backup folder exists
    if not os.path.exists(backup_folder):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backup folder does not exist",
        )
    # Find all *.sqlite3 files in the backup folder
    sqlite_files = glob.glob(os.path.join(backup_folder, "*.sqlite3"))
    sqlite_files.sort(key=os.path.getctime)
    # Delete all backups except the latest one if delete_all_backups is False
    if not delete_all_backups:
        sqlite_files.pop(-1)
    try:
        # Remove each backup file
        for file in sqlite_files:
            os.remove(file)
            logger.info(f"Database backup removed: {file}")
    except Exception as e:
        logger.error(str(e))
        raise
    return sqlite_files

async def clean_database_backups(age_limit: int) -> list:
    # Get the backup folder path
    backup_folder = str(settings.backup_folder)

    # Check if the backup folder exists
    if not os.path.exists(backup_folder):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backup folder does not exist",
        )
    # Find all *.sqlite3 files in the backup folder
    sqlite_files = glob.glob(os.path.join(backup_folder, "*.sqlite3"))
    sqlite_files.sort(key=os.path.getctime)

    # Delete all backups older than age_limit in days

    # target_time = time.time() - age_limit*60*60*24
    target_time = time.time() - age_limit*60*60*1
    older_backups = [file for file in sqlite_files if os.path.getctime(file) < target_time]
    if len(older_backups)>=2:
        try:
            # Remove each backup file
            for file in older_backups:
                os.remove(file)
                logger.info(f"Database backup removed: {file}")
        except Exception as e:
            logger.error(str(e))
            raise
        return older_backups
