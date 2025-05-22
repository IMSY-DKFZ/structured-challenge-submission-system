import os
from urllib.parse import urlparse

from BMC_API.src.core.config.settings import settings


async def create_database() -> None:
    """Create a database."""


async def drop_database(database_url=None) -> None:
    """Drop current database."""
    try:
        if database_url:
            os.remove(urlparse(database_url).path)
        elif settings.db_file.exists():
            os.remove(settings.db_file)
    except:
        pass
