from datetime import datetime
from typing import TypeVar

from pydantic import ConfigDict

from .base_model import NoExtraBaseModel

T = TypeVar("T")


class ChallengeModelBase(NoExtraBaseModel):
    """DTO for challenge base model."""

    challenge_name: str
    challenge_abstract: str | None = None
    challenge_acronym: str | None = None
    challenge_application_scenarios: str | None = None
    challenge_author_names: str | list | None = None
    challenge_author_emails: str | list | None = None
    challenge_doi: str | None = None
    challenge_duration: str | None = None
    challenge_duration_explanation: str | None = None
    challenge_expected_number_of_participants: str | None = None
    challenge_feedback: str | None = None
    challenge_first_feedback_status: str | None = None
    challenge_first_feedback_time: datetime | None = None
    challenge_further_comments: str | None = None
    challenge_interested_in_nvidia_resources: bool | None = False
    challenge_keywords: list | str | None = None
    challenge_novelty: str | None = None
    challenge_owner_id: int | None = None
    challenge_progress: str | None = None
    challenge_publication_and_future: str | None = None
    challenge_references: str | None = None
    challenge_space_and_hardware_requirements: str | None = None
    challenge_workshop: str | None = None
    challenge_year: str | None = None
    challenge_is_lighthouse_challenge: bool | None = False
    challenge_lighthouse_general_terms_agreed: bool | None = False
    challenge_lighthouse_what_is_different: str | None = None
    challenge_lighthouse_closest_challenge: str | None = None
    challenge_lighthouse_test_set_already_used: str | None = None
    challenge_lighthouse_major_scientific_advances: str | None = None
    challenge_lighthouse_clinical_affiliation: str | None = None
    challenge_lighthouse_deadline_for_data: str | None = None
    challenge_lighthouse_prize_money: str | None = None
    challenge_lighthouse_compute_per_participant: str | None = None

    model_config = ConfigDict(from_attributes=True)


# class ChallengeInDB(ChallengeModelBase):
#     """
#     Internal model representing a task stored in the database.
#     This model  is used only for internal operations.
#     """

#     version: int | None = None
#     is_allowed_for_further_editing: bool | None = None
#     challenge_tasks: Any | None = None
#     challenge_locked: bool | None = None
#     challenge_owner: Any | None = None
