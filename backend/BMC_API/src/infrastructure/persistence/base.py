from typing import Any

from sqlalchemy.orm import DeclarativeBase

from BMC_API.src.infrastructure.persistence.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta


def to_dict(obj: Base | None) -> dict[str, Any]:
    if obj is None:
        return {}
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
