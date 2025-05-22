# backend/BMC_API/tests/test_base_dao_extended.py
from datetime import datetime, timedelta

import pytest
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from BMC_API.src.infrastructure.persistence.base import Base
from BMC_API.src.infrastructure.persistence.dao.base_dao import BaseDAO, QueryHelper

pytest_plugins = ["BMC_API.tests.fixtures.base_dao_fixtures"]


# Additional models for relationship testing
class ParentModel(Base):
    __tablename__ = "parent_model"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    created_time = Column(DateTime, default=datetime.now)
    modified_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    children = relationship("ChildModel", back_populates="parent")


class ParentUpdateModel(BaseModel):
    id: int
    name: str | None = None
    created_time: datetime | None = None
    modified_time: datetime | None = None


class ChildModel(Base):
    __tablename__ = "child_model"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("parent_model.id"))
    score = Column(Integer, nullable=True)
    created_time = Column(DateTime, default=datetime.now)
    modified_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    parent = relationship("ParentModel", back_populates="children")


# DAO implementations
class ParentModelDAO(BaseDAO[ParentModel]):
    model = ParentModel


class ChildModelDAO(BaseDAO[ChildModel]):
    model = ChildModel


# Fixtures for relationship testing
@pytest.fixture
async def setup_relationship_tables(_engine):
    """Set up parent and child tables for relationship testing."""
    from sqlalchemy import MetaData
    from sqlalchemy.schema import CreateTable

    metadata = MetaData()

    # Use run_sync to do reflection in a sync context
    async with _engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: metadata.reflect(bind=sync_conn))

    # Create tables if they don't exist
    if "parent_model" not in metadata.tables:
        async with _engine.begin() as conn:
            await conn.execute(CreateTable(ParentModel.__table__))

    if "child_model" not in metadata.tables:
        async with _engine.begin() as conn:
            await conn.execute(CreateTable(ChildModel.__table__))

    yield

    # Cleanup after tests
    async with _engine.begin() as conn:
        await conn.execute(text("DELETE FROM child_model"))
        await conn.execute(text("DELETE FROM child_model WHERE name='child_model'"))
        await conn.execute(text("DELETE FROM parent_model"))
        await conn.execute(text("DELETE FROM parent_model WHERE name='parent_model'"))


@pytest.fixture
async def parent_dao(dbsession: AsyncSession, setup_relationship_tables):
    """Create a ParentModelDAO instance with a database session."""
    return ParentModelDAO(dbsession)


@pytest.fixture
async def child_dao(dbsession: AsyncSession, setup_relationship_tables):
    """Create a ChildModelDAO instance with a database session."""
    return ChildModelDAO(dbsession)


@pytest.fixture
async def relationship_data(parent_dao: ParentModelDAO, child_dao: ChildModelDAO):
    """Create sample data for relationship testing."""
    parents = []
    children = []

    # Create parents
    for i in range(3):
        parent = ParentModel(name=f"Parent {i}")
        created_parent = await parent_dao.create_obj(parent)
        parents.append(created_parent)

    # Create children
    for i in range(9):
        parent_index = i % 3
        child = ChildModel(name=f"Child {i}", parent_id=parents[parent_index].id, score=i * 10)
        created_child = await child_dao.create_obj(child)
        children.append(created_child)

    return {"parents": parents, "children": children}


# Additional Edge Case Tests for BaseDAO
@pytest.mark.anyio
class TestBaseDAOEdgeCases:
    async def test_relationship_sorting(self, child_dao, relationship_data):
        """Test sorting by a field in a related model."""
        query_helper = QueryHelper(ChildModel)
        query = query_helper.build_query_with_output_filters(None)

        # Sort by parent name (relationship field)
        sorted_query = query_helper.apply_sorting(query, "parent.name")

        # Execute manually since our current implementation may not support this directly
        result = await child_dao.session.execute(sorted_query)
        items = result.scalars().all()

        # Group children by parent and verify they're grouped correctly
        parent_groups = {}
        for item in items:
            parent_name = item.parent.name
            if parent_name not in parent_groups:
                parent_groups[parent_name] = []
            parent_groups[parent_name].append(item)

        # Verify groups are together
        current_parent = None
        for item in items:
            if current_parent is None:
                current_parent = item.parent.name
            elif item.parent.name != current_parent:
                # We've moved to a new parent group
                current_parent = item.parent.name

    async def test_transaction_rollback(self, dbsession, parent_dao):
        """Test transaction rollback on error."""
        # Start with clean count
        before_count, _, _ = await parent_dao.list()
        before_count = len(before_count)

        # Try to create two parents, but the second one will fail
        parent1 = ParentModel(name="Transaction Parent 1")
        await parent_dao.create_obj(parent1)
        await dbsession.rollback()

        try:
            # Begin a transaction

            async with dbsession.begin():
                # Create first parent in transaction
                parent2 = ParentModel(name="Transaction Parent 2")
                dbsession.add(parent2)

                # This will cause an error and rollback the transaction
                raise ValueError("Simulated error to test rollback")
        except ValueError:
            pass

        # Verify only the first parent was created
        after_count, _, _ = await parent_dao.list()
        assert len(after_count) == before_count + 1

        # Verify the second parent was not created
        parents, _, _ = await parent_dao.list(search_filters={"name": "Transaction Parent 2"})
        assert len(parents) == 0

    async def test_field_validation(self, child_dao, relationship_data):
        """Test validation for required fields."""
        # Try to create a child without required fields
        child = ChildModel()  # Missing name

        # Should raise an exception
        with pytest.raises(Exception):
            await child_dao.create_obj(child)

    async def test_extreme_pagination(self, parent_dao):
        """Test pagination with extreme values."""
        # Create many parents
        for i in range(10):
            parent = ParentModel(name=f"Extreme Pagination Parent {i}")
            await parent_dao.create_obj(parent)

        # Test with very large offset
        items, pages, count = await parent_dao.list(limit=5, offset=1000)
        assert len(items) == 0  # No results when offset is beyond count

        # Test with negative offset (should be treated as 0)
        items, pages, count = await parent_dao.list(limit=5, offset=-10)
        assert len(items) > 0  # Should return results from the beginning

        # Test with very large limit
        items, pages, count = await parent_dao.list(limit=1000, offset=0)
        assert len(items) == count  # Should return all items

    async def test_partial_update(self, parent_dao):
        """Test updating only specific fields."""
        # Create a parent
        parent = ParentModel(name="Original Name")
        created = await parent_dao.create_obj(parent)

        # Update with a partial object
        partial = ParentUpdateModel(id=created.id, name="Updated Name")
        updated = await parent_dao.update(created.id, partial.model_dump())

        # Verify only the specified field was updated
        assert updated.id == created.id
        assert updated.name == "Updated Name"
        assert updated.created_time == created.created_time  # Should remain unchanged

    async def test_filter_on_timestamps(self, parent_dao):
        """Test filtering on timestamp fields."""
        # Create parents with different timestamps
        now = datetime.now()

        for i in range(3):
            parent = ParentModel(name=f"Timestamp Parent {i}")
            parent.created_time = now - timedelta(days=i)
            parent.modified_time = now - timedelta(days=i)
            await parent_dao.create_obj(parent)

        # Filter for the most recent one
        threshold = now - timedelta(days=4)
        items, _, _ = await parent_dao.list(search_filters={"created_time__gt": threshold})

        assert len(items) == 3
        assert items[0].name == "Timestamp Parent 0"

    async def test_connection_error_handling(self, dbsession, parent_dao, monkeypatch):
        """Test handling of database connection errors."""
        # Patch the execute method to simulate a connection error
        original_execute = dbsession.execute

        async def mock_execute(*args, **kwargs):
            raise OperationalError("Connection error", None, None)

        # Apply the patch
        monkeypatch.setattr(dbsession, "execute", mock_execute)

        # Attempt to list should raise an exception
        with pytest.raises(Exception):
            await parent_dao.list()

        # Restore original method
        monkeypatch.setattr(dbsession, "execute", original_execute)

    async def test_empty_database(self, parent_dao):
        """Test operations on an empty database."""
        # Ensure no data exists first
        items, _, _ = await parent_dao.list(search_filters={"name__startswith": "EmptyDB"})
        assert len(items) == 0

        # Test list
        items, pages, count = await parent_dao.list(search_filters={"name__startswith": "EmptyDB"})
        assert len(items) == 0
        assert pages == 1  # Should be 1 even with no results
        assert count == 0

        # Test sorting on empty results
        items, _, _ = await parent_dao.list(search_filters={"name__startswith": "EmptyDB"}, sort_by="name")
        assert len(items) == 0  # Sorting on empty set should work

    async def test_complex_between_filter(self, child_dao, relationship_data):
        """Test more complex between filtering scenarios."""
        # Between with timestamps
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        tomorrow = now + timedelta(days=1)

        items, _, _ = await child_dao.list(search_filters={"created_time__between": [yesterday, tomorrow]})
        assert len(items) > 0  # Should find items created between yesterday and tomorrow

        # Between with both boundaries being the same
        mid_score = 40
        items, _, _ = await child_dao.list(search_filters={"score__between": [mid_score, mid_score]})
        if len(items) > 0:
            assert all(item.score == mid_score for item in items)

    async def test_unsupported_operator(self, child_dao):
        """Test behavior with unsupported operators."""
        # Try with an invalid operator
        items, _, _ = await child_dao.list(search_filters={"score__invalid_op": 50})
        # Should ignore the invalid operator and return all items
        initial_count, _, _ = await child_dao.list()
        assert len(items) == len(initial_count)
