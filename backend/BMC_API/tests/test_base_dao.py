# backend/BMC_API/tests/test_base_dao.py
from datetime import datetime

import pytest
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, Integer, String, select, text
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from BMC_API.src.infrastructure.persistence.base import Base
from BMC_API.src.infrastructure.persistence.dao.base_dao import BaseDAO, QueryHelper

pytest_plugins = ["BMC_API.tests.fixtures.base_dao_fixtures"]


# Model for testing - renamed to avoid pytest collection
class SampleModel(Base):
    __tablename__ = "test_model"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_time = Column(DateTime, default=datetime.now)
    modified_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    age = Column(Integer, nullable=True)
    category = Column(String, nullable=True)


class SampleUpdateModel(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None
    is_active: bool | None = True
    created_time: datetime | None = None
    modified_time: datetime | None = None
    age: int | None = None
    category: str | None = None


# DAO implementation for SampleModel - renamed to avoid pytest collection
class SampleModelDAO(BaseDAO[SampleModel]):
    model = SampleModel


# Fixtures for test data
@pytest.fixture
async def setup_test_table(_engine):
    """Set up test table for testing."""
    from sqlalchemy import MetaData
    from sqlalchemy.schema import CreateTable

    metadata = MetaData()

    # Use run_sync to do reflection in a sync context
    async with _engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: metadata.reflect(bind=sync_conn))

    # Create SampleModel table if it doesn't exist
    if "test_model" not in metadata.tables:
        async with _engine.begin() as conn:
            await conn.execute(CreateTable(SampleModel.__table__))

    yield

    # Cleanup after tests
    async with _engine.begin() as conn:
        await conn.execute(text(f"DELETE FROM {SampleModel.__tablename__}"))
        await conn.execute(text(f"DELETE FROM {SampleModel.__tablename__} WHERE name='{SampleModel.__tablename__}'"))


@pytest.fixture
async def test_dao(dbsession: AsyncSession, setup_test_table):
    """Create a SampleModelDAO instance with a database session."""
    return SampleModelDAO(dbsession)


@pytest.fixture
async def sample_data(test_dao: SampleModelDAO):
    """Create sample data for testing."""
    test_models = []
    categories = ["A", "B", "C", None]

    for i in range(20):
        model = SampleModel(
            name=f"Test Model {i}",
            description=f"Description for test model {i}" if i % 3 != 0 else None,
            is_active=i % 2 == 0,
            age=i + 20 if i % 5 != 0 else None,
            category=categories[i % 4],
        )
        created_model = await test_dao.create_obj(model)
        test_models.append(created_model)

    return test_models


# Tests for the QueryHelper class


@pytest.mark.anyio
class TestQueryHelper:
    @pytest.fixture
    def query_helper(self):
        return QueryHelper(SampleModel)

    async def test_build_query_with_output_filters(self, query_helper):
        # Test with valid output filters
        query = query_helper.build_query_with_output_filters(["name", "is_active"])
        assert "name" in str(query)
        assert "is_active" in str(query)

        # Test with invalid output filters
        query = query_helper.build_query_with_output_filters(["invalid_field"])
        assert "FROM test_model" in str(query)

        # Test with no output filters
        query = query_helper.build_query_with_output_filters(None)
        assert "FROM test_model" in str(query)

    async def test_apply_search_filters(self, query_helper):
        query = select(SampleModel)

        # Test equality filter
        filtered_query, base_query = query_helper.apply_search_filters(query, {"name": "Test"})
        assert "name = " in str(filtered_query)

        # Test NULL filter
        filtered_query, base_query = query_helper.apply_search_filters(query, {"description": None})
        assert "description IS NULL" in str(filtered_query)

        # Test operators
        operators = {
            "age__gt": 25,
            "age__gte": 25,
            "age__lt": 30,
            "age__lte": 30,
            "age__ge": 30,
            "name__like": "Test",
            "name__ilike": "Test",
            "name__startswith": "T",
            "name__endswith": "T",
            "name__contains": "T",
        }

        for op, val in operators.items():
            filtered_query, base_query = query_helper.apply_search_filters(query, {op: val})
            assert "WHERE" in str(filtered_query), f"Failed for operator {op}"

    async def test_apply_sorting(self, query_helper):
        query = select(SampleModel)

        # Test single field sorting
        sorted_query = query_helper.apply_sorting(query, "name")
        assert "ORDER BY" in str(sorted_query)
        assert "name" in str(sorted_query)

        # Test descending sort
        sorted_query = query_helper.apply_sorting(query, "name", True)
        assert "DESC" in str(sorted_query)

        # Test descending sort with - prefix
        sorted_query = query_helper.apply_sorting(query, "-name")
        assert "DESC" in str(sorted_query)

        # Test multiple fields
        sorted_query = query_helper.apply_sorting(query, "name,age")
        assert "name" in str(sorted_query)
        assert "age" in str(sorted_query)

        # Test with invalid field
        sorted_query = query_helper.apply_sorting(query, "invalid_field")
        assert "ORDER BY" not in str(sorted_query)


# Tests for the BaseDAO class


@pytest.mark.anyio
class TestBaseDAO:
    async def test_get_existing_item(self, test_dao, sample_data):
        # Test retrieving an existing item
        item = await test_dao.get(1)
        assert item is not None
        assert item.id == 1
        assert item.name == "Test Model 0"

    async def test_get_nonexistent_item(self, test_dao):
        # Test retrieving a non-existent item
        item = await test_dao.get(999)
        assert item is None

    async def test_list_all_items(self, test_dao, sample_data):
        # Test listing all items without pagination
        items, total_pages, total_count = await test_dao.list()
        assert len(items) == 20
        assert total_pages == 1
        assert total_count == 20

    async def test_list_with_pagination(self, test_dao, sample_data):
        # Test pagination
        items, total_pages, total_count = await test_dao.list(limit=5, offset=0)
        assert len(items) == 5
        assert total_pages == 4
        assert total_count == 20

        # Test pagination with offset
        items, total_pages, total_count = await test_dao.list(limit=5, offset=5)
        assert len(items) == 5
        assert items[0].id == 6  # Second page

    async def test_list_with_search_filters(self, test_dao, sample_data):
        # Test simple equality filter
        items, _, _ = await test_dao.list(search_filters={"is_active": True})
        assert all(item.is_active for item in items)

        # Test operator filters
        items, _, _ = await test_dao.list(search_filters={"age__gt": 30})
        assert all(item.age > 30 for item in items if item.age is not None)

        # Test NULL filter
        items, _, _ = await test_dao.list(search_filters={"description": None})
        assert all(item.description is None for item in items)

        # Test multiple filters
        items, _, _ = await test_dao.list(search_filters={"is_active": True, "age__gt": 25})
        assert all(item.is_active and (item.age is None or item.age > 25) for item in items)

    async def test_list_with_output_filters(self, test_dao, sample_data):
        # Test selecting specific columns
        items, _, _ = await test_dao.list(output_filters=["id", "name"])
        assert all(isinstance(item, dict) for item in items)
        assert all("id" in item and "name" in item for item in items)
        assert all("description" not in item for item in items)

        # Test with invalid output filters
        items, _, _ = await test_dao.list(output_filters=["invalid_field"])
        assert all(not isinstance(item, dict) for item in items)  # Should return full objects

    async def test_list_with_sorting(self, test_dao, sample_data):
        # Test ascending sort
        items, _, _ = await test_dao.list(sort_by="name")
        for i in range(1, len(items)):
            assert items[i - 1].name <= items[i].name

        # Test descending sort
        items, _, _ = await test_dao.list(sort_by="age", sort_desc=True)
        for i in range(1, len(items)):
            if items[i - 1].age is not None and items[i].age is not None:
                assert items[i - 1].age >= items[i].age

    async def test_create_obj(self, test_dao):
        # Test creating a new object
        model = SampleModel(name="New Test Model", description="New description")
        created = await test_dao.create_obj(model)

        assert created.id is not None
        assert created.name == "New Test Model"
        assert created.description == "New description"
        assert created.created_time is not None
        assert created.modified_time is not None

    async def test_create_obj_integrity_error(self, test_dao, dbsession, monkeypatch):
        # Simulate an integrity error during creation
        original_commit = dbsession.commit

        async def mock_commit():
            await original_commit()
            raise IntegrityError(None, None, None)

        monkeypatch.setattr(dbsession, "commit", mock_commit)

        model = SampleModel(name="Error Model")
        with pytest.raises(Exception):
            await test_dao.create_obj(model)

    async def test_update_obj(self, test_dao, sample_data):
        # Test updating an existing object
        model = await test_dao.get(1)
        original_modified_time = model.modified_time
        original_name = model.name

        # Ensure there's a time difference for the modified_time
        await asyncio_sleep(0.01)

        model.name = "Updated Name"
        updated = await test_dao.update_obj(model)

        assert updated.id == 1
        assert updated.name == "Updated Name"
        assert updated.name != original_name
        assert updated.modified_time > original_modified_time

    async def test_update_nonexistent_item(self, test_dao):
        # Test updating a non-existent item
        model = SampleUpdateModel(id=999, name="Nonexistent")

        with pytest.raises(IndexError):
            await test_dao.update(999, model)

    async def test_update_integrity_error(self, test_dao, sample_data, dbsession, monkeypatch):
        # Simulate an integrity error during update
        original_commit = dbsession.commit

        async def mock_commit():
            await original_commit()
            raise IntegrityError(None, None, None)

        monkeypatch.setattr(dbsession, "commit", mock_commit)

        model = await test_dao.get(1)
        model.name = "Will Fail"

        with pytest.raises(Exception):
            await test_dao.update_obj(model)

    async def test_update(self, test_dao, sample_data):
        # Test the update method that fetches first then updates
        model = SampleUpdateModel(id=1, name="Updated via Update", description="New description")
        updated = await test_dao.update(1, model.model_dump())

        assert updated.id == 1
        assert updated.name == "Updated via Update"
        assert updated.description == "New description"

    async def test_delete_existing_item(self, test_dao, sample_data):
        # Test deleting an existing item
        await test_dao.delete(1)
        deleted_item = await test_dao.get(1)
        assert deleted_item is None

    async def test_delete_nonexistent_item(self, test_dao):
        # Test deleting a non-existent item
        with pytest.raises(NoResultFound):
            await test_dao.delete(999)

    async def test_delete_integrity_error(self, test_dao, sample_data, dbsession, monkeypatch):
        # Simulate an integrity error during deletion
        original_commit = dbsession.commit

        async def mock_commit():
            await original_commit()
            raise IntegrityError(None, None, None)

        monkeypatch.setattr(dbsession, "commit", mock_commit)

        with pytest.raises(Exception):
            await test_dao.delete(1)

    async def test_complex_query_scenario(self, test_dao, sample_data):
        """Test a complex query with multiple filters, sorting and pagination."""
        items, pages, count = await test_dao.list(
            limit=5,
            offset=0,
            search_filters={"is_active": True, "age__gt": 25, "name__like": "Model"},
            output_filters=["id", "name", "age"],
            sort_by="-age",
        )

        # Verify results meet all criteria
        assert all(isinstance(item, dict) for item in items)
        assert all(
            item.get("id") is not None
            and "Model" in item.get("name")
            and (item.get("age") is None or item.get("age") > 25)
            for item in items
        )

        # Verify sorting (descending by age)
        ages = [item.get("age") for item in items if item.get("age") is not None]
        assert all(ages[i] >= ages[i + 1] for i in range(len(ages) - 1))

    async def test_zero_limit_handling(self, test_dao, sample_data):
        """Test handling of zero limit."""
        items, pages, count = await test_dao.list(limit=0)
        assert pages == 1  # Should return 1 page even with limit=0
        assert count == 20
        assert len(items) == count

    async def test_between_operator(self, test_dao, sample_data):
        """Test between operator."""
        items, _, _ = await test_dao.list(search_filters={"age__between": [25, 30]})
        assert all(25 <= item.age <= 30 for item in items if item.age is not None)

    async def test_in_operator(self, test_dao, sample_data):
        """Test in operator."""
        items, _, _ = await test_dao.list(search_filters={"category__in": ["A", "B"]})
        assert all(item.category in ["A", "B"] for item in items)

    async def test_multi_field_sort(self, test_dao, sample_data):
        """Test sorting by multiple fields."""
        # Create some models with the same name but different ages
        for i in range(3):
            model = SampleModel(name="Same Name", age=30 + i)
            await test_dao.create_obj(model)

        items, _, _ = await test_dao.list(search_filters={"name": "Same Name"}, sort_by="name,age")

        assert len(items) == 3
        assert all(item.name == "Same Name" for item in items)
        assert items[0].age < items[1].age < items[2].age


# Helper for async sleep in tests
async def asyncio_sleep(seconds):
    """Helper function for small async delays."""
    import anyio

    await anyio.sleep(seconds)
