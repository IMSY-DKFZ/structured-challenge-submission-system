import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException
from fastapi.responses import FileResponse, StreamingResponse

import BMC_API.src.application.use_cases.challenge_use_cases as challenge_module
from BMC_API.src.api.dependencies.schemas import BulkOperationResponse
from BMC_API.src.application.dto.challenge_dto import (
    ChallengeHistoryModelDTO,
    ChallengeModelBaseOutputDTO,
)
from BMC_API.src.application.dto.task_dto import TaskModelBaseOutputDTO
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
    session = SimpleNamespace(
        commit=AsyncMock(),
        rollback=AsyncMock(),
    )
    repo.session = session
    return repo


@pytest.fixture
def task_repository():
    repo = SimpleNamespace()
    repo.model = SimpleNamespace
    repo.get = AsyncMock()
    repo.list = AsyncMock()
    repo.create_obj = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    repo.session = None  # will be set equal to repository.session in service fixture
    return repo


@pytest.fixture
def task_service(task_repository):
    return TaskService(task_repository, dto_class=TaskModelBaseOutputDTO)


@pytest.fixture
def challenge_history_service():
    return SimpleNamespace(
        list=AsyncMock(),
        delete_bulk=AsyncMock(),
        create=AsyncMock(),
        update=AsyncMock(),
    )


@pytest.fixture
def task_history_service():
    return SimpleNamespace(
        list=AsyncMock(),
        delete_bulk=AsyncMock(),
        create=AsyncMock(),
        update=AsyncMock(),
    )


@pytest.fixture
def service(
    repository,
    task_service,
    challenge_history_service,
    task_history_service,
):
    # Ensure same DB session for transactional methods
    task_service.repository.session = repository.session
    return challenge_module.ChallengeService(
        repository=repository,
        dto_class=ChallengeModelBaseOutputDTO,
        token_cache=None,
        conference_service=None,
        task_service=task_service,
        challenge_history_service=challenge_history_service,
        task_history_service=task_history_service,
        user_service=None,
    )


# challenge_histories
@pytest.mark.anyio
async def test_challenge_histories_success(service, repository):
    history_item = SimpleNamespace(
        id=1,
        challenge_id=1,
        timestamp=datetime.datetime.now(),
        version=1,
        old_status="old",
        new_status="new",
        changes=["a"],
        snapshot={},
    )
    repository.get.return_value = SimpleNamespace(histories=[history_item])

    histories, pages, total = await service.challenge_histories(id=1)

    assert pages == 1 and total == 1
    assert isinstance(histories[0], ChallengeHistoryModelDTO)
    assert histories[0].id == history_item.id


@pytest.mark.anyio
async def test_challenge_histories_no_history(service, repository):
    repository.get.return_value = SimpleNamespace(histories=[])
    with pytest.raises(RepositoryException):
        await service.challenge_histories(id=1)


# update_challenge
@pytest.mark.anyio
async def test_update_challenge_success(service, repository):
    existing = SimpleNamespace(id=1, challenge_name="Test challenge", challenge_status="Draft")
    updated_entity = SimpleNamespace(id=1, challenge_status="DraftUpdated", challenge_name="Changed")
    repository.get.return_value = existing
    repository.update.return_value = updated_entity

    dto = await service.update_challenge(id=1, model_update={"challenge_name": "Changed"})

    assert isinstance(dto, ChallengeModelBaseOutputDTO)
    assert dto.challenge_name == "Changed"
    assert dto.challenge_status == updated_entity.challenge_status
    repository.get.assert_awaited_with(id=1)
    assert repository.get.await_count == 2


@pytest.mark.anyio
async def test_update_challenge_no_id(service):
    with pytest.raises(ValueError):
        await service.update_challenge(id=None, model_update={})


@pytest.mark.anyio
async def test_update_challenge_not_found(service, repository):
    repository.get.return_value = None
    with pytest.raises(NotFoundException):
        await service.update_challenge(id=1, model_update={})


@pytest.mark.anyio
async def test_update_challenge_error(service, repository):
    existing = SimpleNamespace(id=1, challenge_status="Draft")
    repository.get.return_value = existing
    repository.update.side_effect = Exception("db error")
    with pytest.raises(RepositoryException):
        await service.update_challenge(id=1, model_update={})


# update_challenge_bulk
@pytest.mark.anyio
async def test_update_challenge_bulk(service, repository):
    existing = SimpleNamespace(id=1, challenge_name="Test challenge", challenge_status="Draft")
    updated = SimpleNamespace(id=1, challenge_name="Test challenge", challenge_status="DraftUpdated")
    repository.get.side_effect = [existing, existing]
    repository.update.return_value = updated
    updates = [{"id": 1, "challenge_name": "Bulk"}]

    result = await service.update_challenge_bulk(updates)

    assert len(result.successful) == 1
    assert isinstance(result.successful[0], ChallengeModelBaseOutputDTO)
    assert result.successful[0].challenge_status == updated.challenge_status


# prune_challenge
@pytest.mark.anyio
async def test_prune_challenge_success(
    service,
    repository,
    task_service,
    task_history_service,
    challenge_history_service,
):
    history1 = SimpleNamespace(id=100)
    task_history1 = SimpleNamespace(id=200)
    task1 = SimpleNamespace(id=2, task_name="Test task", histories=[task_history1])
    repository.get.return_value = SimpleNamespace(
        challenge_tasks=[task1],
        histories=[history1],
    )

    task_history_service.delete_bulk.return_value = SimpleNamespace(successful=[200], failed=[])
    task_service.delete_bulk = AsyncMock(return_value=SimpleNamespace(successful=[2], failed=[]))
    challenge_history_service.delete_bulk.return_value = SimpleNamespace(successful=[100], failed=[])
    repository.delete.return_value = None

    result = await service.prune_challenge(id=1)

    assert isinstance(result, BulkOperationResponse)
    assert result.successful["task histories"] == [200]
    assert result.successful["tasks"] == [2]
    assert result.successful["challenge histories"] == [100]
    assert result.successful["challenge"] == [1]
    assert result.failed == {}


# download_challenge
@pytest.mark.anyio
async def test_download_challenge_success(service, repository, tmp_path, monkeypatch):
    # Monkeypatch submissions_folder
    monkeypatch.setattr(
        challenge_module.settings,
        "submissions_folder",
        str(tmp_path),
    )
    file_name = "test.pdf"
    (tmp_path / file_name).write_bytes(b"dummy")
    repository.get.return_value = SimpleNamespace(challenge_file=file_name)

    response = await service.download_challenge(id=1)
    assert isinstance(response, FileResponse)
    assert response.media_type == "application/pdf"
    assert response.headers["X-Content-Filename"] == file_name


@pytest.mark.anyio
async def test_download_challenge_not_found(service, repository, tmp_path, monkeypatch):
    monkeypatch.setattr(
        challenge_module.settings,
        "submissions_folder",
        str(tmp_path),
    )
    repository.get.return_value = SimpleNamespace(challenge_file="nofile.pdf")

    with pytest.raises(HTTPException) as exc:
        await service.download_challenge(id=1)
    assert exc.value.status_code == 404


# download_challenge_bulk
@pytest.mark.anyio
async def test_download_challenge_bulk_no_files(service, repository):
    repository.get.return_value = SimpleNamespace(challenge_file=None)
    with pytest.raises(HTTPException) as exc:
        await service.download_challenge_bulk(ids=[1, 2])
    assert exc.value.status_code == 404


@pytest.mark.anyio
async def test_download_challenge_bulk_success(service, repository, tmp_path, monkeypatch):
    monkeypatch.setattr(
        challenge_module.settings,
        "submissions_folder",
        str(tmp_path),
    )
    file_name = "a.pdf"
    (tmp_path / file_name).write_bytes(b"data")
    repository.get.side_effect = [
        SimpleNamespace(challenge_file=file_name),
    ]

    response = await service.download_challenge_bulk(ids=[1])
    assert isinstance(response, StreamingResponse)
    assert response.media_type == "application/zip"
    assert response.headers["Content-Disposition"] == "attachment; filename=challenges_bulk_download.zip"
    assert response.headers["X-Successful-IDs"] == "1"
    assert response.headers["X-Failed-Count"] == "0"


# status
@pytest.mark.anyio
async def test_status_success(service, repository, task_service):
    challenge_obj = SimpleNamespace(
        id=1,
        challenge_name="Test challenge",
        challenge_status="Draft",
        challenge_tasks=[SimpleNamespace(id=2)],
    )
    updated_entity = SimpleNamespace(id=1, challenge_name="Test challenge updated", challenge_status="DraftUpdated")
    repository.get.side_effect = [challenge_obj, challenge_obj]
    repository.update.return_value = updated_entity
    task_service.update_bulk = AsyncMock()

    result = await service.status(id=1, new_status="DraftUpdated")
    assert isinstance(result, ChallengeModelBaseOutputDTO)
    assert result.challenge_status == "DraftUpdated"
    task_service.update_bulk.assert_awaited_once()
    repository.update.assert_awaited_once()


@pytest.mark.anyio
async def test_status_session_mismatch(repository, task_service):
    repository.session = object()
    task_service.repository.session = object()
    service_mis = challenge_module.ChallengeService(
        repository=repository,
        dto_class=ChallengeModelBaseOutputDTO,
        token_cache=None,
        conference_service=None,
        task_service=task_service,
        challenge_history_service=None,
        task_history_service=None,
        user_service=None,
    )
    with pytest.raises(ValueError):
        await service_mis.status(id=1, new_status="X")


# bulk_status
@pytest.mark.anyio
async def test_bulk_status_success(service, repository, task_service):
    challenge_obj = SimpleNamespace(
        id=1,
        challenge_status="Draft",
        challenge_tasks=[SimpleNamespace(id=3)],
    )
    updated_entity = SimpleNamespace(id=1, challenge_name="Test challenge updated", challenge_status="DraftUpdated")
    repository.get.side_effect = [challenge_obj, challenge_obj]
    repository.update.return_value = updated_entity
    task_service.update_bulk = AsyncMock()

    result = await service.bulk_status(ids=[1], new_status="DraftUpdated")
    assert len(result.successful) == 1
    assert isinstance(result.successful[0], ChallengeModelBaseOutputDTO)
    assert result.failed == []
    task_service.update_bulk.assert_awaited_once()


@pytest.mark.anyio
async def test_bulk_status_session_mismatch(repository, task_service):
    repository.session = object()
    task_service.repository.session = object()
    service_mis = challenge_module.ChallengeService(
        repository=repository,
        dto_class=ChallengeModelBaseOutputDTO,
        token_cache=None,
        conference_service=None,
        task_service=task_service,
        challenge_history_service=None,
        task_history_service=None,
        user_service=None,
    )
    with pytest.raises(ValueError):
        await service_mis.bulk_status(ids=[1], new_status="X")


# take_snapshot
@pytest.mark.anyio
async def test_take_snapshot_calls_ops(service, repository):
    challenge_obj = SimpleNamespace(
        id=1,
        challenge_status="Draft",
        challenge_tasks=[SimpleNamespace(id=5)],
    )
    repository.get.return_value = challenge_obj
    service.submission_ops.detect_differences = AsyncMock(return_value=(["c_diff"], ["t_diff"]))
    service.submission_ops.take_snapshot = AsyncMock()

    await service.take_snapshot(id=1)
    service.submission_ops.detect_differences.assert_awaited_once_with(
        new_status=challenge_obj.challenge_status,
        status_assignments=[],
        challenge_obj=challenge_obj,
        task_list=challenge_obj.challenge_tasks,
    )
    service.submission_ops.take_snapshot.assert_awaited_once_with(
        new_status=challenge_obj.challenge_status,
        current_status=challenge_obj.challenge_status,
        status_assignments=[],
        differences_in_challenge=["c_diff"],
        differences_in_tasks=["t_diff"],
        challenge_obj=challenge_obj,
        task_list=challenge_obj.challenge_tasks,
    )


# submit_challenge
@pytest.mark.anyio
async def test_submit_challenge_success(
    service,
    repository,
    task_service,
    tmp_path,
    monkeypatch,
    challenge_history_service,
    task_history_service,
):
    # Prepare challenge object
    challenge_obj = SimpleNamespace(
        id=1,
        challenge_name="Name",
        challenge_file="existing.pdf",
        challenge_status="Draft",
        version=1,
        challenge_tasks=[],
        challenge_conference=SimpleNamespace(chairperson_emails=[]),
        challenge_owner=SimpleNamespace(email="u@test.com", first_name="F", last_name="L"),
    )
    # repository.get for get_raw and for update existence
    repository.get.side_effect = [challenge_obj, challenge_obj]

    # Monkeypatch status and assignments
    monkeypatch.setattr(
        challenge_module.StatusActions,
        "next_status_for_submit",
        lambda x: "New",
    )
    monkeypatch.setattr(
        challenge_module.StatusBusiness,
        "status_assignments",
        lambda x: [challenge_module.Assignments.EXPORT_PROPOSAL],
    )

    # Monkeypatch submission ops
    service.submission_ops.detect_differences = AsyncMock(return_value=([], []))
    service.submission_ops.mark_differences = lambda a, b, c, d, e: (c, d)
    service.submission_ops.take_snapshot = AsyncMock()

    # Monkeypatch PDF export
    monkeypatch.setattr(
        challenge_module,
        "convert_challenge_to_pdf",
        lambda cp, tl: "file.pdf",
    )
    monkeypatch.setattr(
        challenge_module.settings,
        "submissions_folder",
        str(tmp_path),
    )
    # Create dummy file
    (tmp_path / "file.pdf").write_bytes(b"pdf")

    # Prepare update return
    updated_entity = SimpleNamespace(
        id=1,
        challenge_name="Test challenge",
        challenge_status="DraftUpdated",
        challenge_submission_time=datetime.datetime.now(),
        version=2,
        challenge_file="file.pdf",
    )
    repository.update.return_value = updated_entity

    # Call submit_challenge
    result = await service.submit_challenge(
        id=1,
        background_tasks=SimpleNamespace(add_task=lambda x: None),
        send_notification_emails=False,
    )

    assert isinstance(result, ChallengeModelBaseOutputDTO)
    assert result.challenge_file == "file.pdf"
    repository.update.assert_awaited_once()
