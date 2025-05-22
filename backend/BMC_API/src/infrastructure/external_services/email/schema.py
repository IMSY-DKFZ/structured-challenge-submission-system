from typing import Any, Dict, List

from pydantic import BaseModel, EmailStr, Field


class EmailSchema(BaseModel):
    subject: str
    sender: EmailStr | None = Field(
        default=None,
        title="**Optional** Email address to be used as sender.",
    )
    recipients: List[EmailStr]
    template_body: Dict[str, Any] | None = Field(
        default=None,
        title="**Optional** Dictionary containing variable names and their values for HTML template.",
        example='{"first_name": "Fred", "last_name": "Fredsson"}',
    )

    body: str | None = Field(
        default=None,
        title="**Optional** Plain text body of the email.",
        example="Hello, this is a plain text email.",
    )
    attachments: List[str] | None = Field(
        default=[],
        title="**Optional** List of paths to files to be attached to the email.",
        example="['/path/to/file1', '/path/to/file2']",
    )
    reply_to: List[EmailStr] | None = Field(
        default=[],
        title="**Optional** Email address to be used as reply-to.",
        example="william.cushing@altostrat.com",
    )
