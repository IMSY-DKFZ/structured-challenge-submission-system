# backend/BMC_API/src/application/dto/user_dto.py
"""
Data Transfer Objects (DTOs) for /user endpoint

*UserPasswordDTO: Specific password model with a validator function for validating the password field.
*UserCreateDTO: Used for creating new user model.
*UserUpdateDTO: Used for updating existing user models.
*UserResponseDTO: Used for returning user models in API responses.
*UserCreateAdminDTO: Extension of UserCreateDTO.
*UserUpdateAdminDTO: Extension of UserUpdateDTO.
*UserResponseAdminDTO: Used for responses returning user models with whole fields except password.
*Token: Used for returning access tokens in API responses. Used for Authentication interface.
*TokenData: Used to store data about a user's access token. Used for Authentication interface.
"""

import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, Json, validator

from BMC_API.src.api.schemas.user_schema import UserInDB, UserModelBase
from BMC_API.src.application.dto.dependencies import create_all_optional_model
from BMC_API.src.domain.value_objects.enums.user_enums import Roles


class UserPasswordDTO(BaseModel):
    password: str = Field(..., description="User's password.")

    @validator("password")
    def password_validator(cls, password):
        errors = ""
        if len(password) < 8:
            errors += " Password must be at least 8 characters long."
        if not re.search("[a-z]", password):
            errors += " Password must contain at least one lower case letter."
        if not re.search("[A-Z]", password):
            errors += " Password must contain at least one upper case letter."
        if not re.search("[0-9]", password):
            errors += " Password must contain at least one digit."
        if not re.search(r"[!@#$%^&*()\-_+={}[\]|;':\",.\/<>?`~\\]", password):
            errors += " Password must contain at least one special character."
        if (
            "abc" in password.lower()
            or "xyz" in password.lower()
            or "qwert" in password.lower()
            or "123" in password
            or "987" in password
        ):
            errors += (
                " This password contains too simple pattern such as 'abc' or '123'. Please select a strong password."
            )
        if errors:
            errors = "Following problem(s) found with the password:" + errors
            raise ValueError(errors)
        return password


class UserCreateDTO(UserPasswordDTO, UserModelBase):
    """
    DTO for creating a new user.
    Extends the base user model with required fields for creation.
    """

    email: EmailStr = Field(..., description="User's email address.")
    first_name: str = Field(..., description="User's first name.")
    last_name: str = Field(..., description="User's last name.")

    @validator("email")
    def convert_email_to_lowercase(cls, email):
        return email.lower()


class UserUpdateDTO(UserPasswordDTO, UserModelBase):
    """
    DTO for updating an existing user.
    All fields are optional.
    """

    password: Optional[str] = Field(None, description="User's password.")


class UserResponseDTO(UserModelBase):
    """
    DTO for returning user details in API responses.
    """

    email: Optional[EmailStr] = Field(None, description="User's email address.")
    created_time: Optional[datetime] = Field(None, description="Timestamp when the user was created.")
    last_login_time: Optional[datetime] = Field(None, description="Timestamp of the user's last login.")
    modified_time: Optional[datetime] = Field(None, description="Timestamp when the user was last modified.")
    notifications: Optional[Json] = Field(None, description="User's notification settings.")
    roles: Optional[List] = Field(
        None, description="List of roles assigned to the user."
    )

    model_config = ConfigDict(from_attributes=True)


UserCreateDTO_Optional = create_all_optional_model(model_name="UserCreateDTO_Optional", base_model=UserCreateDTO)


class UserCreateAdminDTO(UserCreateDTO_Optional):
    """
    DTO for admin operations when creating a new user.
    Extends the standard user creation DTO with additional admin-specific fields.
    """

    disabled: Optional[bool] = Field(False, description="Whether the user account is disabled.")
    email_confirmed: Optional[bool] = Field(True, description="Whether the user's email is confirmed.")
    reset_token: Optional[str] = Field(None, description="Token used for password reset.")
    email_confirmation_token: Optional[str] = Field(None, description="Token used for email confirmation.")
    roles: Optional[List[Roles]] = Field(
        default_factory=lambda: [Roles.ORGANIZER],
        description="List of roles assigned to the user.",
    )


class UserUpdateAdminDTO(UserCreateAdminDTO):
    """
    DTO for admin operations when updating an existing user.
    """

    email_confirmation_token: Optional[str] = Field(None, description="Token used for email confirmation.")
    roles: Optional[List[Roles]] = Field(None,  description="List of roles assigned to the user.",
    )


UserResponseAdminDTO = create_all_optional_model(model_name="UserResponseAdminDTO", base_model=UserInDB)


# Schemas for authentication interface
class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token.")
    refresh_token: str = Field(..., description="JWT refresh token.")
    token_type: str = Field("bearer", description="Type of the token (bearer).")


class TokenData(BaseModel):
    email: Optional[EmailStr] = Field(None, description="Email associated with the token.")
