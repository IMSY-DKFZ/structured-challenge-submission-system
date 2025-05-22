# BMC_API/src/api/dependencies/route_dependencies.py
from typing import Annotated, Callable, Optional, Type, TypeVar

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from BMC_API.src.domain.interfaces.token_cache import TokenCache
from BMC_API.src.infrastructure.persistence.dependencies import get_db_session

# Define type variables for repository and service.
RepoT = TypeVar("RepoT")
ServiceT = TypeVar("ServiceT")


def get_repository(repository_class: Type[RepoT]) -> Callable[..., RepoT]:
    """
    Generic dependency that creates a repository instance given a repository class.
    Assumes that the repository class accepts an AsyncSession in its constructor.
    """

    def dependency(session: Annotated[AsyncSession, Depends(get_db_session)]) -> RepoT:
        return repository_class(session)

    return dependency


def get_service(
    service_class: Type[ServiceT],
    repository_dependency: Callable[..., RepoT],
    dto_class: Optional[Type] = None,
    token_cache: Optional[TokenCache] = None,
) -> Callable[..., ServiceT]:
    """
    Generic dependency that creates a service instance given a service class and a repository dependency.
    Assumes that the service class accepts the repository instance in its constructor.
    """

    def dependency(
        repository: Annotated[RepoT, Depends(repository_dependency)],
    ) -> ServiceT:
        kwargs = {"repository": repository}
        if dto_class is not None:
            if not issubclass(dto_class, BaseModel):
                raise ValueError(f"{dto_class.__name__} must be a subclass of pydantic.BaseModel")
            kwargs["dto_class"] = dto_class
        if token_cache is not None:
            kwargs["token_cache"] = token_cache

        return service_class(**kwargs)

    return dependency
