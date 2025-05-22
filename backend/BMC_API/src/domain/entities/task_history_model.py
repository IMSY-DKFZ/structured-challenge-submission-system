from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import JSON, DateTime, Integer, String

from BMC_API.src.infrastructure.persistence.base import Base


class TaskHistoryModel(Base):
    """Model for task histories."""

    __tablename__ = "task_histories"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    challenge_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    old_status = Column(String)
    new_status = Column(String)
    version = Column(Integer)
    task = relationship("TaskModel", back_populates="histories", lazy="selectin")
    changes = Column(JSON)
    snapshot = Column(JSON)
