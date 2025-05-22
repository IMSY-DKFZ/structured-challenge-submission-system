# backend/BMC_API/src/domain/entities/user_model.py
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import JSON, Boolean, DateTime, Integer, String, Text

from BMC_API.src.api.dependencies.functions import get_random_digits
from BMC_API.src.domain.value_objects.enums.user_enums import Roles
from BMC_API.src.infrastructure.persistence.base import Base


class UserModel(Base):
    """Model for users."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    bio = Column(Text)
    challenges = relationship("ChallengeModel", back_populates="challenge_owner", lazy="selectin")
    city = Column(String(100))
    conferences = relationship("ConferenceModel", back_populates="owner", lazy="selectin")
    country = Column(String(100))
    created_time = Column(DateTime, nullable=False)
    disabled = Column(Boolean, default=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    email_confirmation_token = Column(String(100))
    email_confirmed = Column(Boolean, default=False)
    first_name = Column(String(50))
    institution = Column(String(100))
    last_login_time = Column(DateTime)
    last_name = Column(String(50))
    modified_time = Column(DateTime)
    newsletter = Column(Boolean, default=False)
    notes = Column(Text)
    notifications = Column(JSON)
    password = Column(String(100), nullable=False)
    reset_token = Column(String(100), unique=True)
    roles = Column(JSON, default=[Roles.ORGANIZER])
    tasks = relationship("TaskModel", back_populates="task_owner", lazy="selectin")
    titel = Column(String(10))
    token_expiry = Column(DateTime)
    website = Column(String(100))

    @classmethod
    def create_new(cls, email: str, password: str, first_name: str, last_name: str, **kwargs) -> "UserModel":
        """
        Factory method to create a new UserModel instance.
        Applies domain defaults and generates an email confirmation token.
        """
        now = datetime.now()

        return cls(
            email=email.lower(),
            password=password,
            first_name=first_name,
            last_name=last_name,
            email_confirmed=kwargs.pop("email_confirmed", False),
            disabled=kwargs.pop("disabled", False),
            email_confirmation_token=kwargs.pop("email_confirmation_token", cls.generate_confirmation_token()),
            created_time=kwargs.pop("created_time", now),
            modified_time=kwargs.pop("modified_time", now),
            roles=kwargs.pop("roles", [Roles.ORGANIZER]),
            **kwargs,
        )

    @staticmethod
    def generate_confirmation_token() -> str:
        """
        Generate an email confirmation token.
        """
        return get_random_digits(6)

    # def change_password(
    #     self, current_password: str, new_password: str, password_hasher: PasswordHasher
    # ) -> None:
    #     """
    #     Validates the current password and updates the user password using the provided hasher.
    #     """
    #     if not password_hasher.verify(current_password, self.password):
    #         raise InvalidCredentialsException("Current password does not match.")
    #     self.password = password_hasher.hash(new_password)
