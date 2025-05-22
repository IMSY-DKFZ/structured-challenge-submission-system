from typing import List

from pydantic import ConfigDict, EmailStr

from .base_model import NoExtraBaseModel


class MessageDTO(NoExtraBaseModel):
    """MessageDTO model."""

    message: str
    subject: str | None = None
    recipients_group: str
    sender_name: str | None = None
    sender_email: EmailStr

class Message(MessageDTO):
    """Message model."""

    recipients: List[str]
    model_config = ConfigDict(extra="allow")
    
