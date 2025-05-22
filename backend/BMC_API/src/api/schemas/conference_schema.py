from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, Field

from .base_model import NoExtraBaseModel


class ConferenceModelBase(NoExtraBaseModel):
    """
    Base schema for the Conference object.
    """

    name: str = Field(..., description="The full name of the conference.")
    information: Optional[str] = Field(
        None, description="Additional details about the conference."
    )
    venue: Optional[str] = Field(None, description="The venue of the conference.")
    city: Optional[str] = Field(
        None, description="The city where the conference is held."
    )
    country: Optional[str] = Field(
        None, description="The country where the conference is held."
    )
    proposal_start_date: datetime = Field(
        ..., description="Start date for proposal submissions."
    )
    proposal_end_date: datetime = Field(
        ..., description="End date for proposal submissions."
    )
    start_date: datetime = Field(..., description="Start date of the conference.")
    short_name: str = Field(
        ..., description="A short name or abbreviation for the conference."
    )
    end_date: datetime = Field(..., description="End date of the conference.")
    year: int = Field(..., description="The year in which the conference is held.")
    is_lighthouse_challenge: bool = Field(
        False,
        description="Flag indicating if this is a lighthouse challenge conference.",
    )
    is_open_for_submissions: bool = Field(
        True, description="Flag indicating if the conference is open for submissions."
    )

    model_config = ConfigDict(from_attributes=True)
