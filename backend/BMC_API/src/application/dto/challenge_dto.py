# backend/BMC_API/src/application/dto/challenge_dto.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from BMC_API.src.api.schemas.challenge_schema import ChallengeModelBase
from BMC_API.src.application.dto.dependencies import create_all_optional_model
from BMC_API.src.application.dto.task_dto import TaskModelBaseOutputDTO
from BMC_API.src.application.dto.user_dto import UserResponseDTO
from BMC_API.src.domain.value_objects.enums.challenge_enums import ChallengeStatus

# Models for user access


class ChallengeModelBaseOutputDTO(ChallengeModelBase):
    """
    Output DTO for the Conference model with basic fields.
    Returned when accessing conference models via the API.
    """

    id: int | None = None
    version: int | None = None
    is_allowed_for_further_editing: bool | None = None
    challenge_name: str | None = None
    challenge_conference_id: int | None = None
    challenge_created_time: datetime | None = None
    challenge_file: str | None = None
    challenge_modified_time: datetime | None = None
    challenge_status: ChallengeStatus | None = None
    challenge_submission_time: datetime | None = None
    challenge_tasks: list[TaskModelBaseOutputDTO] | None = None
    challenge_interested_in_nvidia_resources: bool | None = None
    challenge_is_lighthouse_challenge: bool | None = None
    challenge_lighthouse_general_terms_agreed: bool | None = None

    model_config = ConfigDict(from_attributes=True)


class ChallengeModelOutputPdfDTO(ChallengeModelBaseOutputDTO):
    """
    DTO for challenge models while exporting PDF file.

    It returned when accessing challenge models from the API.
    """

    subheading: str | None = None


class ChallengeModelCreateDTO(ChallengeModelBase):
    """DTO for creating new challenge model."""

    # challenge_conference_id: int | None = None
    # challenge_owner_id: int | None = None

    model_config = ConfigDict(from_attributes=False)


ChallengeModelUpdateDTO: BaseModel = create_all_optional_model(model_name="ChallengeModelUpdateDTO", base_model=ChallengeModelBase)


class ChallengeModelStatusUpdateDTO(BaseModel):
    """DTO for updating challenge status."""

    challenge_status: ChallengeStatus = ChallengeStatus.DRAFT
    # challenge_locked: bool | None = False

    class Config:
        use_enum_values = True


# Models for admin access


class ChallengeInputAdminDTO(ChallengeModelCreateDTO):
    """DTO for creating/updating new challenge model."""

    challenge_locked: bool | None = None
    version: int | None = None
    # challenge_owner_id: int | None = None
    is_allowed_for_further_editing: bool | None = None
    model_config = ConfigDict(from_attributes=False, extra='allow')

ChallengeUpdateAdminDTO: BaseModel = create_all_optional_model(model_name="ChallengeUpdateAdminDTO", base_model=ChallengeInputAdminDTO)

class ChallengeResponseAdminDTO(ChallengeModelBaseOutputDTO):
    """
    DTO for detailed conference model responses for admin operations.
    Returned when accessing conference models via the API.
    """

    challenge_owner: UserResponseDTO | dict | None = None

    model_config = ConfigDict(from_attributes=True)


# Models for history entities


class ChallengeHistoryModelDTO(BaseModel):
    id: int | None = None
    challenge_id: int | None = None
    timestamp: datetime | None = None
    version: int | None = None
    old_status: str | None = None
    new_status: str | None = None
    challenge: ChallengeModelBaseOutputDTO | None = None
    changes: list | None = None
    snapshot: dict | None = None
    model_config = ConfigDict(from_attributes=True)


class ChallengeHistoryFilters(BaseModel):
    id: Optional[int] = None
    challenge_id: Optional[int] = None
    timestamp: Optional[datetime] | Optional[str] = None
    old_status: Optional[str] = None
    new_status: Optional[str] = None
    version: Optional[int] = None
