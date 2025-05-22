import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# Import the test models
from BMC_API.tests.test_base_dao import SampleModel


@pytest.fixture
async def clean_database(_engine):
    """Ensure we start with a clean database for each test suite."""
    # Create tables if they don't exist
    tables = [SampleModel.__tablename__, "parent_model", "child_model"]

    async with _engine.begin() as conn:
        for table in tables:
            try:
                await conn.execute(text(f"DELETE FROM {table}"))
                await conn.execute(text(f"DELETE FROM {table} WHERE name='{table}'"))
            except Exception:
                # Table might not exist yet, which is okay
                pass

    yield


@pytest.fixture
async def benchmark_data(dbsession: AsyncSession):
    """Create a large dataset for performance testing."""
    # Create the test table if needed
    from sqlalchemy.schema import CreateTable

    try:
        async with dbsession.begin():
            await dbsession.execute(CreateTable(SampleModel.__table__))
    except Exception:
        pass
