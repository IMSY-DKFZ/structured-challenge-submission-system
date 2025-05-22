from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import JSON, Boolean, DateTime, Integer, String, Text

from BMC_API.src.infrastructure.persistence.base import Base


class ConferenceModel(Base):
    """Model for conferences."""

    __tablename__ = "conferences"

    id = Column(Integer, primary_key=True, index=True)
    challenges = relationship(
        "ChallengeModel", back_populates="challenge_conference", lazy="selectin"
    )
    city = Column(String(length=255))
    country = Column(String(length=255))
    created_time = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    information = Column(String(length=2000))
    is_lighthouse_challenge = Column(Boolean, default=False)
    is_open_for_submissions = Column(Boolean, default=True)
    message_before_generate_proposal = Column(Text)
    modified_time = Column(DateTime)
    name = Column(String(length=255), unique=True)
    owner = relationship("UserModel", back_populates="conferences", lazy="selectin")
    owner_id = Column(Integer, ForeignKey("users.id"))
    proposal_start_date = Column(DateTime)
    proposal_end_date = Column(DateTime)
    short_name = Column(String(length=255))
    start_date = Column(DateTime)
    venue = Column(String(length=255))
    chairperson_emails = Column(JSON)
    chairperson_names = Column(JSON)
    year = Column(Integer)
