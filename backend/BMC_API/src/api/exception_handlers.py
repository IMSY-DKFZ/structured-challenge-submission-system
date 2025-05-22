# backend/BMC_API/src/api/exception_handlers.py
from fastapi import Request, status
from fastapi.responses import JSONResponse

from BMC_API.src.core.exceptions import (
    ConferenceLockedException,
    InvalidCredentialsException,
    InvalidTokenException,
    NotFoundException,
    RepositoryException,
    UserAlreadyExistsException,
    UserNotAuthenticatedException,
    UserNotAuthorizedException,
    UserNotFoundException,
)

auth_header = {"WWW-Authenticate": "Bearer"}


def register_exception_handlers(app):
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"},
        )

    @app.exception_handler(RepositoryException)
    async def repository_exception_handler(request: Request, exc: RepositoryException):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)})

    @app.exception_handler(NotFoundException)
    async def entity_not_found_exception_handler(request: Request, exc: NotFoundException):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

    @app.exception_handler(UserNotFoundException)
    async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

    @app.exception_handler(UserNotAuthenticatedException)
    async def user_not_authenticates_exception_handler(request: Request, exc: UserNotAuthenticatedException):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc)})

    @app.exception_handler(UserNotAuthorizedException)
    async def user_not_authhorized_exception_handler(request: Request, exc: UserNotAuthorizedException):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(exc)})

    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exist_exception_handler(request: Request, exc: UserAlreadyExistsException):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)},
            headers=auth_header,
        )

    @app.exception_handler(InvalidTokenException)
    async def invalid_token_exception_handler(request: Request, exc: InvalidTokenException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)},
            headers=auth_header,
        )

    @app.exception_handler(ConferenceLockedException)
    async def conference_locked_exception_handler(request: Request, exc: ConferenceLockedException):
        return JSONResponse(
            status_code=status.HTTP_423_LOCKED,
            content={"detail": str(exc)},
            headers=auth_header,
        )
