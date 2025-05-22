from pydantic import BaseModel


class RedisValueDTO(BaseModel):
    """DTO for redis values."""

    key: str
    value: str | None  # noqa: WPS110


class RedisExistsDTO(BaseModel):
    """DTO for redis existence."""

    key_exists: bool | None  # noqa: WPS110
