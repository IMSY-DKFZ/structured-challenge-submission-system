# backend/BMC_API/src/api/schemas/user_schema.py
"""
Base schemas for /user endpoint.
The models in "BMC_API.src.application.dto.user_dto" are inherited from these models

*UserModelBase: Base user model
*UserInDB: Used to represent a user in the database. Used for internal ops and admin endpoints.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict, EmailStr, Field, Json

from BMC_API.src.domain.value_objects.enums.user_enums import Roles

from .base_model import NoExtraBaseModel


class UserModelBase(NoExtraBaseModel):
    """
    Base model for user data used in requests.
    """

    bio: Optional[str] = Field(None, description="Short biography of the user.")
    city: Optional[str] = Field(None, description="City of the user.")
    country: Optional[str] = Field(None, description="Country of the user.")
    first_name: Optional[str] = Field(None, description="User's first name.")
    institution: Optional[str] = Field(
        None, description="Institution affiliated with the user."
    )
    last_name: Optional[str] = Field(None, description="User's last name.")
    newsletter: Optional[bool] = Field(
        False, description="Whether the user is subscribed to the newsletter."
    )
    titel: Optional[str] = Field(None, description="User's title.")
    website: Optional[str] = Field(None, description="User's website URL.")


class UserInDB(UserModelBase):
    """
    Internal model representing a user stored in the database.
    This model excludes the password field and is used only for internal operations.
    """

    id: int = Field(..., description="Unique identifier for the user.")
    created_time: Optional[datetime] = Field(
        None, description="Timestamp when the user was created."
    )
    disabled: Optional[bool] = Field(
        False, description="Flag indicating if the user account is disabled."
    )
    email: EmailStr = Field(..., description="User's email address.")
    email_confirmation_token: Optional[str] = Field(
        None, description="Token used for email confirmation."
    )
    email_confirmed: Optional[bool] = Field(
        False, description="Flag indicating if the user's email is confirmed."
    )
    last_login_time: Optional[datetime] = Field(
        None, description="Timestamp of the last login."
    )
    modified_time: Optional[datetime] = Field(
        None, description="Timestamp when the user was last modified."
    )
    notes: Optional[str] = Field(None, description="Additional notes about the user.")
    notifications: Optional[Json] = Field(
        None, description="User's notification settings in JSON format."
    )
    reset_token: Optional[str] = Field(
        None, description="Token used for password reset."
    )
    roles: Optional[List[Roles]] = Field(
        None, description="List of roles assigned to the user."
    )
    token_expiry: Optional[datetime] = Field(
        None, description="Expiry time of the user's token."
    )

    model_config = ConfigDict(from_attributes=True)
