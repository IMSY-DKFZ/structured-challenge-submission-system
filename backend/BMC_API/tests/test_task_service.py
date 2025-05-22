# backend/BMC_API/tests/test_task_service.py
import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import NoResultFound

from BMC_API.src.application.dto.task_dto import (
    TaskHistoryModelDTO,
    TaskModelBaseOutputDTO,
)
from BMC_API.src.application.use_cases.task_use_cases import TaskService
from BMC_API.src.core.exceptions import NotFoundException, RepositoryException


@pytest.fixture
def repository():
    repo = SimpleNamespace()
    repo.model = SimpleNamespace
    repo.get = AsyncMock()
    repo.list = AsyncMock()
    repo.create_obj = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    repo.session = object()
    return repo


@pytest.fixture
def service(repository):
    return TaskService(repository, dto_class=TaskModelBaseOutputDTO)


@pytest.mark.anyio
async def test_get_raw_success(service, repository):
    entity = SimpleNamespace(id=1, task_name="Test", task_created_time=datetime.datetime.now())
    repository.get.return_value = entity

    result = await service.get_raw(id=1)

    assert result is entity
    repository.get.assert_awaited_once_with(id=1)


@pytest.mark.anyio
async def test_get_raw_no_id(service):
    with pytest.raises(ValueError):
        await service.get_raw(id=None)


@pytest.mark.anyio
async def test_get_raw_not_found(service, repository):
    repository.get.return_value = None
    with pytest.raises(NotFoundException) as exc:
        await service.get_raw(id=1)
    assert f"{repository.model.__name__} with id 1 not found." in str(exc.value)


@pytest.mark.anyio
async def test_get_success(service, repository):
    now = datetime.datetime.now()
    entity = SimpleNamespace(id=1, task_name="Test", task_created_time=now)
    repository.get.return_value = entity

    dto = await service.get(id=1)

    assert isinstance(dto, TaskModelBaseOutputDTO)
    assert dto.id == entity.id
    assert dto.task_name == entity.task_name
    assert dto.task_created_time == entity.task_created_time
    repository.get.assert_awaited_once_with(id=1)


@pytest.mark.anyio
async def test_get_error_wrapped(service, repository):
    repository.get.side_effect = Exception("db error")
    with pytest.raises(RepositoryException) as exc:
        await service.get(id=1)
    assert "Error getting entity" in str(exc.value)


@pytest.mark.anyio
async def test_list_success(service, repository):
    now = datetime.datetime.now()
    e1 = SimpleNamespace(id=1, task_name="T1", task_created_time=now)
    e2 = SimpleNamespace(id=2, task_name="T2", task_created_time=now)
    repository.list.return_value = ([e1, e2], 1, 2)

    dtos, pages, total = await service.list(limit=10, offset=0)

    assert pages == 1 and total == 2
    assert all(isinstance(d, TaskModelBaseOutputDTO) for d in dtos)
    assert [d.id for d in dtos] == [1, 2]


@pytest.mark.anyio
async def test_list_not_found(service, repository):
    repository.list.return_value = ([], 0, 0)
    with pytest.raises(NotFoundException):
        await service.list(limit=10, offset=0)


@pytest.mark.anyio
async def test_create_success(service, repository):
    now = datetime.datetime.now()

    def create_side_effect(obj):
        obj.id = 1
        return obj

    repository.create_obj.side_effect = create_side_effect
    data = {"task_name": "New", "task_created_time": now}

    dto = await service.create(model_create=data)

    assert isinstance(dto, TaskModelBaseOutputDTO)
    assert dto.id == 1
    assert dto.task_name == "New"


@pytest.mark.anyio
async def test_create_error(service, repository):
    repository.create_obj.side_effect = Exception("db error")
    with pytest.raises(RepositoryException):
        await service.create(model_create={"task_name": "New", "task_created_time": datetime.datetime.now()})


@pytest.mark.anyio
async def test_update_task_success(service, repository):
    now = datetime.datetime.now()
    existing = SimpleNamespace(id=1, task_name="Old", task_created_time=now, task_status="Draft")
    updated_entity = SimpleNamespace(id=1, task_name="Updated", task_created_time=now, task_status="DRAFT_UPDATED")

    repository.get.return_value = existing
    repository.update.return_value = updated_entity

    dto = await service.update_task(id=1, model_update={"task_name": "Updated"})

    assert isinstance(dto, TaskModelBaseOutputDTO)
    assert dto.task_name == "Updated"
    assert dto.task_status == "DRAFT_UPDATED"
    repository.get.assert_awaited_with(id=1)
    assert repository.get.await_count == 2


@pytest.mark.anyio
async def test_update_task_no_id(service):
    with pytest.raises(ValueError):
        await service.update_task(id=None, model_update={})


@pytest.mark.anyio
async def test_update_task_not_found(service, repository):
    repository.get.return_value = None
    with pytest.raises(NotFoundException):
        await service.update_task(id=1, model_update={"task_name": "X"})


@pytest.mark.anyio
async def test_update_task_error(service, repository):
    existing = SimpleNamespace(id=1, task_name="Old", task_created_time=datetime.datetime.now(), task_status="NEW")
    repository.get.return_value = existing
    repository.update.side_effect = Exception("db error")

    with pytest.raises(RepositoryException):
        await service.update_task(id=1, model_update={"task_name": "X"})


@pytest.mark.anyio
async def test_update_task_bulk(service, repository):
    now = datetime.datetime.now()
    e1 = SimpleNamespace(id=1, task_name="U1", task_created_time=now, task_status="Draft")
    u1 = SimpleNamespace(id=1, task_name="U1-updated", task_created_time=now, task_status="DRAFT_UPDATED")

    repository.get.side_effect = [e1, e1]
    repository.update.return_value = u1

    updates = [{"id": 1, "task_name": "U1-updated"}]

    result = await service.update_task_bulk(updates)

    assert len(result.successful) == 1
    assert result.successful[0].id == 1
    assert result.successful[0].task_status == "DRAFT_UPDATED"


@pytest.mark.anyio
async def test_delete_success(service, repository):
    repository.delete.return_value = None
    await service.delete(id=1)
    repository.delete.assert_awaited_once_with(id=1)


@pytest.mark.anyio
async def test_delete_no_id(service):
    with pytest.raises(ValueError):
        await service.delete(id=None)


@pytest.mark.anyio
async def test_delete_not_found(service, repository):
    repository.delete.side_effect = NoResultFound()
    with pytest.raises(NotFoundException):
        await service.delete(id=1)


@pytest.mark.anyio
async def test_delete_error(service, repository):
    repository.delete.side_effect = Exception("db error")
    with pytest.raises(RepositoryException):
        await service.delete(id=1)


@pytest.mark.anyio
async def test_delete_bulk(service, repository):
    # id=1 succeeds, id=2 raises NoResultFound
    def delete_side_effect(id):
        if id == 2:
            raise NoResultFound()
        return None

    repository.delete.side_effect = delete_side_effect

    result = await service.delete_bulk([1, 2])

    assert result.successful == [1]
    assert len(result.failed) == 1
    assert result.failed[0]["id"] == 2


@pytest.mark.anyio
async def test_check_ownership_true(service, repository):
    entity = SimpleNamespace(task_owner_id=10)
    repository.get.return_value = entity

    assert await service.check_ownership(10, 1, "task_owner_id") is True


@pytest.mark.anyio
async def test_check_ownership_not_found(service, repository):
    repository.get.return_value = None
    with pytest.raises(NotFoundException):
        await service.check_ownership(10, 1, "task_owner_id")


@pytest.mark.anyio
async def test_check_ownership_attr_error(service, repository):
    entity = SimpleNamespace(other_field=10)
    repository.get.return_value = entity
    with pytest.raises(AttributeError):
        await service.check_ownership(10, 1, "task_owner_id")


@pytest.mark.anyio
async def test_task_histories_success(service, repository):
    history_item = SimpleNamespace(
        id=1,
        task_id=1,
        challenge_id=1,
        timestamp=datetime.datetime.now(),
        version=1,
        old_status="old",
        new_status="new",
        changes=["a"],
        snapshot=None,
    )
    obj = SimpleNamespace(histories=[history_item])
    repository.get.return_value = obj

    histories, pages, total = await service.task_histories(id=1)

    assert pages == 1 and total == 1
    assert isinstance(histories[0], TaskHistoryModelDTO)
    assert histories[0].id == 1


@pytest.mark.anyio
async def test_task_histories_no_history(service, repository):
    obj = SimpleNamespace(histories=[])
    repository.get.return_value = obj

    with pytest.raises(RepositoryException):
        await service.task_histories(id=1)
