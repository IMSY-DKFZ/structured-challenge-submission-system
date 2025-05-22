# backend/BMC_API/src/api/routes/contact.py

from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from starlette import status

from BMC_API.src.api.dependencies.route_dependencies import get_repository, get_service
from BMC_API.src.api.schemas.contact_schema import Message, MessageDTO
from BMC_API.src.application.interfaces.email_scheduler import EmailSchedulerService
from BMC_API.src.application.use_cases.conference_use_cases import ConferenceService
from BMC_API.src.application.use_cases.user_use_cases import UserService
from BMC_API.src.core.config.settings import settings
from BMC_API.src.core.exceptions import NotFoundException
from BMC_API.src.domain.value_objects.enums.user_enums import Roles
from BMC_API.src.infrastructure.persistence.dao.conference_dao import (
    SQLAlchemyConferenceRepository,
)
from BMC_API.src.infrastructure.persistence.dao.user_dao import SQLAlchemyUserRepository

# Dependency functions
user_repository_dependency = get_repository(SQLAlchemyUserRepository)
user_service_dependency = get_service(UserService, user_repository_dependency)

conference_repository_dependency = get_repository(SQLAlchemyConferenceRepository)
conference_service_dependency = get_service(ConferenceService, conference_repository_dependency)

# Router
router = APIRouter()


@router.post("/")
async def send_message(
    incoming_message: MessageDTO,
    background_tasks: BackgroundTasks,
    user_service: Annotated[UserService, Depends(user_service_dependency)],
    conference_service: Annotated[ConferenceService, Depends(conference_service_dependency)],
) -> JSONResponse:
    """
    Sends email to selected recipient group.

    **Parameters:**

    * `incoming_message`: incoming message.

    **Returns:**

    * Result of operation.
    """
    try:
        incoming_message_dict = incoming_message.model_dump()
        if incoming_message_dict["recipients_group"] == "Challenge chairs":
            try:
                open_conferences, *_  = await conference_service.list(search_filters={"is_open_for_submissions": True})
                if open_conferences:
                    recipients = set()
                    for conference in open_conferences:
                        recipients.update(conference.chairperson_emails)
                    incoming_message_dict["recipients"] = list(recipients)
                    message=Message(**incoming_message_dict)
            except NotFoundException:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"detail": "No active conference found."},
                )
            except Exception as e:
                raise e
        elif incoming_message_dict["recipients_group"] == "Technical support":
            admin_list, *_ = await user_service.list(search_filters={"roles__contains": Roles.ADMIN})
            if admin_list and not isinstance(admin_list, list) and isinstance(admin_list, str):
                admin_list = [admin_list]

            # Clear fake e-mail address of DEFAULT_ADMIN_NAME
            admin_emails = [admin.email for admin in admin_list if admin.email != settings.DEFAULT_ADMIN_NAME]
            
            incoming_message_dict["recipients"] = list(set(admin_emails))

            message=Message(**incoming_message_dict)
        else:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": "Invalid recipient type"},
            )

        email_scheduler = EmailSchedulerService(background_tasks)
        email_scheduler.schedule_contact_message(message)
    except Exception as e:
        raise e
    return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Your message has been sent successfully."},
            )