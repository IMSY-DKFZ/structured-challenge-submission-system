# application/interfaces/authorization.py

from typing import Callable, List, Type

from fastapi import Depends

from BMC_API.src.api.schemas.user_schema import UserInDB
from BMC_API.src.application.use_cases.base_use_cases import BaseService
from BMC_API.src.core.exceptions import UserNotAuthorizedException

from .authentication import get_current_active_user_dependency


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: UserInDB = Depends(get_current_active_user_dependency)):
        if not user or not any(role in self.allowed_roles for role in user.roles):
            raise UserNotAuthorizedException


def ownership_checker_dependency(
    service_class: Type[BaseService],
    model_id_field: str,
    repository_dependency: Callable,
    get_model_id: Callable[[int], int],
):
    """
    Factory that returns a FastAPI dependency which verifies that the current user
    is the owner of the requested resource.

    Args:
        service_class: The Service class that implements check_ownership().
        model_id_field: The name of the ownership field (e.g., 'task_owner_id').
        repository_dependency: Callable dependency returning the repository.
        get_model_id: Callable that extracts model_id from route parameters.

    Returns:
        A dependency function that raises UserNotAuthorizedException if unauthorized.
    """

    async def dependency(
        id: int,
        current_user: UserInDB = Depends(get_current_active_user_dependency),
        repository=Depends(repository_dependency),
    ):
        service = service_class(repository)
        owns = await service.check_ownership(
            user_id=current_user.id,
            model_id=get_model_id(id),
            model_id_field=model_id_field,
        )

        if not owns:
            raise UserNotAuthorizedException

        return True

    return dependency
