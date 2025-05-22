from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict, EmailStr, Field

from BMC_API.src.api.schemas.conference_schema import ConferenceModelBase
from BMC_API.src.application.dto.dependencies import create_all_optional_model


class ConferenceModelBaseOutputDTO(ConferenceModelBase):
    """
    Output DTO for the Conference model with basic fields.
    Returned when accessing conference models via the API.
    """

    id: int = Field(..., description="Unique identifier of the conference.")


class ConferenceCreateAdminDTO(ConferenceModelBase):
    """
    DTO for creating a new conference model.
    """

    chairperson_emails: List[EmailStr] = Field(..., description="List of chairperson email addresses.")
    chairperson_names: Optional[List[str]] = Field(None, description="List of chairperson names.")
    message_before_generate_proposal: Optional[str] = Field(
        None, description="Message to display before generating a proposal."
    )

    model_config = ConfigDict(from_attributes=False)


ConferenceUpdateAdminDTO = create_all_optional_model(
    model_name="ConferenceUpdateAdminDTO", base_model=ConferenceCreateAdminDTO
)


class ConferenceResponseAdminDTO(ConferenceUpdateAdminDTO):
    """
    DTO for detailed conference model responses for admin operations.
    Returned when accessing conference models via the API.
    """

    id: int = Field(None, description="Unique identifier of the conference.")
    created_time: Optional[datetime] = Field(None, description="Timestamp when the conference was created.")
    modified_time: Optional[datetime] = Field(None, description="Timestamp when the conference was last modified.")
    owner_id: Optional[int] = Field(None, description="Identifier of the owner of the conference.")

    model_config = ConfigDict(from_attributes=True)
