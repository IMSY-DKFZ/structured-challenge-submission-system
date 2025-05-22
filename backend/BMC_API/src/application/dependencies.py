# application/dependencies.py
from fastapi import Depends

from BMC_API.src.api.dependencies.route_dependencies import get_repository
from BMC_API.src.application.dto.challenge_dto import (
    ChallengeModelBaseOutputDTO,
    ChallengeResponseAdminDTO,
)
from BMC_API.src.application.use_cases.challenge_history_use_cases import (
    ChallengeHistoryService,
)
from BMC_API.src.application.use_cases.challenge_use_cases import ChallengeService
from BMC_API.src.application.use_cases.conference_use_cases import ConferenceService
from BMC_API.src.application.use_cases.task_history_use_cases import TaskHistoryService
from BMC_API.src.application.use_cases.task_use_cases import TaskService
from BMC_API.src.application.use_cases.user_use_cases import UserService
from BMC_API.src.domain.repositories.challenge_history_repository import (
    ChallengeHistoryRepositoryProtocol,
)
from BMC_API.src.domain.repositories.challenge_repository import (
    ChallengeRepositoryProtocol,
)
from BMC_API.src.domain.repositories.conference_repository import (
    ConferenceRepositoryProtocol,
)
from BMC_API.src.domain.repositories.task_history_repository import (
    TaskHistoryRepositoryProtocol,
)
from BMC_API.src.domain.repositories.task_repository import TaskRepositoryProtocol
from BMC_API.src.domain.repositories.user_repository import UserRepositoryProtocol
from BMC_API.src.infrastructure.persistence.dao.challenge_dao import (
    SQLAlchemyChallengeRepository,
)
from BMC_API.src.infrastructure.persistence.dao.challenge_history_dao import (
    SQLAlchemyChallengeHistoryRepository,
)
from BMC_API.src.infrastructure.persistence.dao.conference_dao import (
    SQLAlchemyConferenceRepository,
)
from BMC_API.src.infrastructure.persistence.dao.task_dao import SQLAlchemyTaskRepository
from BMC_API.src.infrastructure.persistence.dao.task_history_dao import (
    SQLAlchemyTaskHistoryRepository,
)
from BMC_API.src.infrastructure.persistence.dao.user_dao import SQLAlchemyUserRepository


def get_challenge_service(
    conference_repo: ConferenceRepositoryProtocol = Depends(get_repository(SQLAlchemyConferenceRepository)),
    challenge_repo: ChallengeRepositoryProtocol = Depends(get_repository(SQLAlchemyChallengeRepository)),
    task_repo: TaskRepositoryProtocol = Depends(get_repository(SQLAlchemyTaskRepository)),
    challenge_history_repo: ChallengeHistoryRepositoryProtocol = Depends(
        get_repository(SQLAlchemyChallengeHistoryRepository)
    ),
    task_history_repo: TaskHistoryRepositoryProtocol = Depends(get_repository(SQLAlchemyTaskHistoryRepository)),
    user_repo: UserRepositoryProtocol = Depends(get_repository(SQLAlchemyUserRepository)),
):
    # build the helpers
    conference_svc = ConferenceService(conference_repo)
    task_svc = TaskService(task_repo)
    challenge_hist_svc = ChallengeHistoryService(challenge_history_repo)
    task_hist_svc = TaskHistoryService(task_history_repo)
    user_svc = UserService(user_repo)
    # finally build the main service
    return ChallengeService(
        repository=challenge_repo,
        dto_class=ChallengeModelBaseOutputDTO,
        # now pass in all the helpers it needs:
        conference_service=conference_svc,
        task_service=task_svc,
        challenge_history_service=challenge_hist_svc,
        task_history_service=task_hist_svc,
        user_service=user_svc,
    )

def get_challenge_service_admin(
    conference_repo: ConferenceRepositoryProtocol = Depends(get_repository(SQLAlchemyConferenceRepository)),
    challenge_repo: ChallengeRepositoryProtocol = Depends(get_repository(SQLAlchemyChallengeRepository)),
    task_repo: TaskRepositoryProtocol = Depends(get_repository(SQLAlchemyTaskRepository)),
    challenge_history_repo: ChallengeHistoryRepositoryProtocol = Depends(
        get_repository(SQLAlchemyChallengeHistoryRepository)
    ),
    task_history_repo: TaskHistoryRepositoryProtocol = Depends(get_repository(SQLAlchemyTaskHistoryRepository)),
    user_repo: UserRepositoryProtocol = Depends(get_repository(SQLAlchemyUserRepository)),
):
    # build the helpers
    conference_svc = ConferenceService(conference_repo)
    task_svc = TaskService(task_repo)
    challenge_hist_svc = ChallengeHistoryService(challenge_history_repo)
    task_hist_svc = TaskHistoryService(task_history_repo)
    user_svc = UserService(user_repo)
    # finally build the main service
    return ChallengeService(
        repository=challenge_repo,
        dto_class=ChallengeResponseAdminDTO,
        # now pass in all the helpers it needs:
        conference_service=conference_svc,
        task_service=task_svc,
        challenge_history_service=challenge_hist_svc,
        task_history_service=task_hist_svc,
        user_service=user_svc,
    )
