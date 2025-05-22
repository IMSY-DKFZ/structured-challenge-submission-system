# backend/BMC_API/src/core/exceptions/__init__.py

"""
DO NOt forget to register new exceptions into
backend/BMC_API/src/api/exception_handlers.py file!
"""

from typing import Optional


class RepositoryException(Exception):
    """General exception for repository errors."""

    default_message: str = "A repository error occurred."

    def __init__(self, message: Optional[str] = None) -> None:
        # Use the default message if none is provided.
        if message is None:
            message = self.default_message
        self.message = message
        super().__init__(message)


class UserNotFoundException(RepositoryException):
    """Exception raised when a user is not found."""

    default_message: str = "User not found."

    def __init__(self, user_id: Optional[int] = None, message: Optional[str] = None) -> None:
        if message is None:
            if user_id is not None:
                message = f"User with id {user_id} not found."
            else:
                message = self.default_message
        self.user_id = user_id
        super().__init__(message)


class NotFoundException(RepositoryException):
    """Exception raised when a user is not found."""

    default_message: str = "Entity not found."

    def __init__(self, user_id: Optional[int] = None, message: Optional[str] = None) -> None:
        if message is None:
            if user_id is not None:
                message = f"Entity with id {user_id} not found."
            else:
                message = self.default_message
        self.user_id = user_id
        super().__init__(message)


class UserNotAuthenticatedException(RepositoryException):
    """Exception raised when a user is not authenticated."""

    default_message: str = "Not authenticated."

    def __init__(self, message: Optional[str] = None) -> None:
        if message is None:
            message = self.default_message
        super().__init__(message)


class UserNotAuthorizedException(RepositoryException):
    """Exception raised when a user is not authenticated."""

    default_message: str = "You don't have permission to access this resource."

    def __init__(self, message: Optional[str] = None) -> None:
        if message is None:
            message = self.default_message
        super().__init__(message)


class UserAlreadyExistsException(RepositoryException):
    """Exception raised when a duplicate user is detected."""

    default_message: str = "User already exists."

    def __init__(self, email: Optional[str] = None, message: Optional[str] = None) -> None:
        if message is None:
            if email is not None:
                message = f"User with email {email} already exists."
            else:
                message = self.default_message
        super().__init__(message)


class InvalidCredentialsException(RepositoryException):
    """Exception raised for invalid login credentials."""

    default_message: str = "Could not validate credentials."

    def __init__(self, message: Optional[str] = None) -> None:
        if message is None:
            message = self.default_message
        super().__init__(message)


class InvalidTokenException(RepositoryException):
    """Exception raised for invalid tokens."""

    default_message: str = "Incorrect token."

    def __init__(self, message: Optional[str] = None) -> None:
        if message is None:
            message = self.default_message
        super().__init__(message)


class ConferenceLockedException(RepositoryException):
    """Exception raised if conference is not open for submissions."""

    default_message: str = "Challenge proposal is closed for further changes. The submission deadline has passed."

    def __init__(self, message: Optional[str] = None) -> None:
        if message is None:
            message = self.default_message
        super().__init__(message)
