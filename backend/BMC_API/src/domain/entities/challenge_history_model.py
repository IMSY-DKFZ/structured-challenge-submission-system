from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import JSON, DateTime, Integer, String

from BMC_API.src.infrastructure.persistence.base import Base


class ChallengeHistoryModel(Base):
    """Model for challenge histories."""

    __tablename__ = "challenge_histories"

    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    old_status = Column(String)
    new_status = Column(String)
    version = Column(Integer)
    challenge = relationship(
        "ChallengeModel", back_populates="histories", lazy="selectin"
    )
    changes = Column(JSON)
    snapshot = Column(JSON)
