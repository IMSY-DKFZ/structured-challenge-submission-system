# backend/BMC_API/src/application/dto/task_dto.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from BMC_API.src.api.schemas.task_schema import TaskModelBase
from BMC_API.src.application.dto.dependencies import create_all_optional_model


class TaskModelBaseOutputDTO(TaskModelBase):
    """
    Output DTO for the Task model with basic fields.
    Returned when accessing conference models via the API.
    """

    id: int | None = None
    version: int | None = None
    task_name: str | None = None
    task_created_time: datetime | None = None
    task_modified_time: datetime | None = None
    task_status: str | None = None
    task_submission_time: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class TaskModelCreateDTO(TaskModelBase):
    """DTO for creating new task model."""

    model_config = ConfigDict(from_attributes=False)


TaskModelUpdateDTO: BaseModel = create_all_optional_model(model_name="TaskModelUpdateDTO", base_model=TaskModelBase)


class TaskInputAdminDTO(TaskModelCreateDTO):
    """
    DTO for creating/updating a new conference model.
    """

    version: int | None = None
    task_challenge_id: int | None = None
    task_locked: bool | None = None
    task_owner_id: int | None = None

    model_config = ConfigDict(from_attributes=True, extra='allow')

TaskUpdateAdminDTO: BaseModel = create_all_optional_model(model_name="TaskUpdateAdminDTO", base_model=TaskInputAdminDTO)

class TaskResponseAdminDTO(TaskModelBaseOutputDTO):
    """
    DTO for detailed conference model responses for admin operations.
    Returned when accessing conference models via the API.
    """
    task_challenge_id: int | None = None
    # task_challenge: Any | None = None
    task_locked: bool | None = None
    task_owner_id: int | None = None
    # task_owner: Any | None = None

    model_config = ConfigDict(from_attributes=True)


class TaskHistoryModelDTO(BaseModel):
    id: int | None = None
    task_id: int | None = None
    challenge_id: int | None = None
    timestamp: datetime | None = None
    version: int | None = None
    old_status: str | None = None
    new_status: str | None = None
    task: TaskModelBaseOutputDTO | None = None
    changes: list | None = None
    snapshot: dict | None = None
    model_config = ConfigDict(from_attributes=True)


class TaskHistoryFilters(BaseModel):
    id: Optional[int] = None
    task_id: Optional[int] = None
    challenge_id: Optional[int] = None
    timestamp: Optional[datetime] | Optional[str] = None
    old_status: Optional[str] = None
    new_status: Optional[str] = None
    version: Optional[int] = None
