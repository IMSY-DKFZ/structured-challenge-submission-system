from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import JSON, Boolean, DateTime, Integer, String

from BMC_API.src.domain.value_objects.enums.challenge_enums import ChallengeStatus
from BMC_API.src.infrastructure.persistence.base import Base


class ChallengeModel(Base):
    """Model for challenges."""

    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(Integer, default=1)
    histories = relationship(
        "ChallengeHistoryModel", back_populates="challenge", lazy="selectin"
    )
    is_allowed_for_further_editing = Column(Boolean, default=False)
    challenge_created_time = Column(DateTime, nullable=False)
    challenge_modified_time = Column(DateTime)
    challenge_abstract = Column(String)
    challenge_acronym = Column(String(length=255))
    challenge_application_scenarios = Column(String)
    challenge_author_emails = Column(JSON)
    challenge_author_names = Column(JSON)
    challenge_conference = relationship(
        "ConferenceModel", back_populates="challenges", lazy="selectin"
    )
    challenge_conference_id = Column(Integer, ForeignKey("conferences.id"))
    challenge_doi = Column(String(length=255))
    challenge_duration = Column(String)
    challenge_duration_explanation = Column(String)
    challenge_expected_number_of_participants = Column(String)
    challenge_feedback = Column(String)
    challenge_file = Column(String)
    challenge_first_feedback_status = Column(String)
    challenge_first_feedback_time = Column(DateTime)
    challenge_further_comments = Column(String)
    challenge_interested_in_nvidia_resources = Column(Boolean)
    challenge_keywords = Column(JSON)
    challenge_locked = Column(Boolean, default=False)
    challenge_name = Column(String)
    challenge_novelty = Column(String)
    challenge_owner = relationship(
        "UserModel", back_populates="challenges", lazy="selectin"
    )
    challenge_owner_id = Column(Integer, ForeignKey("users.id"))
    challenge_progress = Column(String)
    challenge_publication_and_future = Column(String)
    challenge_references = Column(String)
    challenge_reviewer_status = Column(String)
    # challenge_short_name = Column(String(length=255))
    challenge_space_and_hardware_requirements = Column(String)
    challenge_status = Column(String, default=ChallengeStatus.DRAFT)
    challenge_submission_time = Column(DateTime)
    challenge_super_reviewer_status = Column(String)
    challenge_tasks = relationship(
        "TaskModel", back_populates="task_challenge", lazy="selectin"
    )
    challenge_workshop = Column(String)
    challenge_year = Column(String)
    challenge_is_lighthouse_challenge = Column(Boolean, default=False)
    challenge_lighthouse_general_terms_agreed = Column(Boolean, default=False)
    challenge_lighthouse_what_is_different = Column(String)
    challenge_lighthouse_closest_challenge = Column(String)
    challenge_lighthouse_test_set_already_used = Column(String)
    challenge_lighthouse_major_scientific_advances = Column(String)
    challenge_lighthouse_clinical_affiliation = Column(String)
    challenge_lighthouse_deadline_for_data = Column(String)
    challenge_lighthouse_prize_money = Column(String)
    challenge_lighthouse_compute_per_participant = Column(String)
