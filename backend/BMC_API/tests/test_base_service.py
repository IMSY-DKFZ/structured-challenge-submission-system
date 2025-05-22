# backend/BMC_API/tests/test_base_service.py
from unittest.mock import AsyncMock

import pytest
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound

from BMC_API.src.api.dependencies.schemas import BulkOperationResponse
from BMC_API.src.application.use_cases.base_use_cases import BaseService
from BMC_API.src.core.exceptions import NotFoundException, RepositoryException


class DummyModel:
    def __init__(self, id, name, owner_id=None):
        self.id = id
        self.name = name
        self.owner_id = owner_id


class DummyDTO(BaseModel):
    id: int
    name: str

    @classmethod
    def model_validate(cls, obj):
        return cls(id=obj.id, name=obj.name)


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def base_service(mock_repo):
    return BaseService(repository=mock_repo, dto_class=DummyDTO)


@pytest.mark.anyio
async def test_get_success(base_service, mock_repo):
    mock_repo.get.return_value = DummyModel(1, "Test")
    result = await base_service.get(1)
    assert isinstance(result, DummyDTO)
    assert result.name == "Test"


@pytest.mark.anyio
async def test_get_not_found(base_service, mock_repo):
    mock_repo.get.return_value = None
    with pytest.raises(RepositoryException):
        await base_service.get(999)


@pytest.mark.anyio
async def test_get_raw_success(base_service, mock_repo):
    mock_repo.get.return_value = DummyModel(1, "Raw Test")
    result = await base_service.get_raw(1)
    assert isinstance(result, DummyModel)
    assert result.name == "Raw Test"


@pytest.mark.anyio
async def test_get_raw_not_found(base_service, mock_repo):
    mock_repo.get.return_value = None
    with pytest.raises(NotFoundException):
        await base_service.get_raw(123)


@pytest.mark.anyio
async def test_list_success(base_service, mock_repo):
    mock_repo.list.return_value = (
        [{"id": 1, "name": "One"}, {"id": 2, "name": "Two"}],  # <- dicts, not DummyModel
        1,
        2,
    )

    results, total_pages, total_records = await base_service.list()

    assert len(results) == 2
    assert total_pages == 1
    assert total_records == 2
    assert isinstance(results[0], DummyDTO)


@pytest.mark.anyio
async def test_create_success(base_service, mock_repo):
    mock_repo.model = DummyModel
    mock_repo.create_obj.return_value = DummyModel(10, "Created")

    data = {"id": 10, "name": "Created"}
    result = await base_service.create(data)

    assert isinstance(result, DummyDTO)
    assert result.id == 10


@pytest.mark.anyio
async def test_update_success(base_service, mock_repo):
    mock_repo.get.return_value = DummyModel(1, "Before")
    mock_repo.update.return_value = DummyModel(1, "After")

    result = await base_service.update(1, {"name": "After"})
    assert isinstance(result, DummyDTO)
    assert result.name == "After"


@pytest.mark.anyio
async def test_update_not_found(base_service, mock_repo):
    mock_repo.get.return_value = None

    with pytest.raises(NotFoundException):
        await base_service.update(123, {"name": "Doesn't matter"})


@pytest.mark.anyio
async def test_delete_success(base_service, mock_repo):
    await base_service.delete(1)
    mock_repo.delete.assert_awaited_once_with(id=1)


@pytest.mark.anyio
async def test_delete_not_found(base_service, mock_repo):
    mock_repo.delete.side_effect = NoResultFound()
    with pytest.raises(NotFoundException):
        await base_service.delete(123)


@pytest.mark.anyio
async def test_delete_bulk_mixed(base_service, mock_repo):
    def delete_side_effect(id):
        if id == 1:
            return None
        else:
            raise Exception("fail")

    mock_repo.delete.side_effect = delete_side_effect

    result = await base_service.delete_bulk([1, 2])

    assert 1 in result.successful
    assert len(result.failed) == 1


@pytest.mark.anyio
async def test_check_ownership_success(base_service, mock_repo):
    mock_repo.get.return_value = DummyModel(99, "Item", owner_id=5)
    owns = await base_service.check_ownership(user_id=5, model_id=99, model_id_field="owner_id")
    assert owns is True


@pytest.mark.anyio
async def test_check_ownership_false(base_service, mock_repo):
    mock_repo.get.return_value = DummyModel(99, "Item", owner_id=8)
    owns = await base_service.check_ownership(user_id=3, model_id=99, model_id_field="owner_id")
    assert owns is False


@pytest.mark.anyio
async def test_update_bulk_success_baseservice(base_service, mock_repo):
    updates = [
        {"id": 1, "name": "Updated 1"},
        {"id": 2, "name": "Updated 2"},
    ]

    mock_repo.get.side_effect = [
        DummyModel(1, "Original 1"),
        DummyModel(2, "Original 2"),
    ]

    mock_repo.update.side_effect = [
        DummyModel(1, "Updated 1"),
        DummyModel(2, "Updated 2"),
    ]

    result: BulkOperationResponse = await base_service.update_bulk(updates)

    assert len(result.successful) == 2
    assert len(result.failed) == 0
    assert result.successful[0].name == "Updated 1"


@pytest.mark.anyio
async def test_update_bulk_missing_id_baseservice(base_service):
    updates = [{"name": "No ID"}]

    result = await base_service.update_bulk(updates)

    assert len(result.successful) == 0
    assert len(result.failed) == 1
    assert "missing" in result.failed[0]["error"].lower()


@pytest.mark.anyio
async def test_update_bulk_entity_not_found_baseservice(base_service, mock_repo):
    updates = [{"id": 99, "name": "Not Found"}]
    mock_repo.get.return_value = None

    result = await base_service.update_bulk(updates)

    assert len(result.successful) == 0
    assert len(result.failed) == 1
    assert "not found" in result.failed[0]["error"].lower()


@pytest.mark.anyio
async def test_update_bulk_partial_failure_baseservice(base_service, mock_repo):
    updates = [{"id": 1, "name": "Updated A"}, {"id": 2, "name": "Updated B"}]

    mock_repo.get.side_effect = [
        DummyModel(1, "Original A"),
        None,  # Second item doesn't exist
    ]
    mock_repo.update.return_value = DummyModel(1, "Updated A")

    result = await base_service.update_bulk(updates)

    assert len(result.successful) == 1
    assert len(result.failed) == 1
    assert result.successful[0].id == 1
    assert result.failed[0]["data"]["id"] == 2
