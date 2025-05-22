from datetime import datetime
from typing import List

from email_validator import EmailNotValidError
from fastapi import BackgroundTasks, HTTPException, status
from loguru import logger

from BMC_API.src.api.schemas.contact_schema import Message
from BMC_API.src.core.config.settings import settings
from BMC_API.src.domain.entities.user_model import UserModel
from BMC_API.src.infrastructure.external_services.email.email_service import (
    email_sender,
)
from BMC_API.src.infrastructure.external_services.email.schema import EmailSchema


class EmailSchedulerService:
    def __init__(self, background_tasks: BackgroundTasks):
        self.background_tasks = background_tasks

    def schedule_contact_message(self, incoming_message: Message) -> None:
        try:
            # Sanitize subject, message and name
            message = incoming_message.message
            message.replace("<", "&lt;")
            message.replace(">", "&gt;")
            message.replace("\n", "<br />")

            subject = incoming_message.subject
            subject.replace("<", "&lt;")
            subject.replace(">", "&gt;")

            sender_name = incoming_message.sender_name
            sender_name.replace("<", "&lt;")
            sender_name.replace(">", "&gt;")

            # Check recipients is a valid list
            recipients = incoming_message.recipients
            if not isinstance(recipients, list):
                recipients = [recipients]

            # Check reply_to is a valid list
            reply_to = incoming_message.sender_email
            if not isinstance(reply_to, list):
                reply_to = [reply_to]

            email_schema = EmailSchema(
                recipients=recipients,
                subject=incoming_message.subject,
                reply_to=reply_to,
                template_body={
                    "message": incoming_message.message,
                    "sender_name": sender_name,
                    "sender_email": incoming_message.sender_email,
                    "subject": incoming_message.subject,
                    "recipients_group": incoming_message.recipients_group,
                },
            )

            if settings.environment != "dev":
                # * Add to background tasks
                self.background_tasks.add_task(email_sender, email=email_schema, template_name="contact_page.html")
                logger.info(f"E-mail scheduled to {email_schema.recipients}")
            else:
                logger.debug("E-mail scheduled:")
                logger.debug(email_schema)
        except EmailNotValidError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email address is not valid",
            )
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Something went wrong. Please contact the admins",
            )

    def schedule_email_confirmation(self, user: UserModel) -> None:
        """
        Prepares and schedules the email confirmation task.
        """
        # Prepare the recipient(s)
        recipients = user.email
        if recipients and not isinstance(recipients, list) and isinstance(recipients, str):
            recipients = [recipients]

        # Build the variables for e-mail template.
        email_confirmation_url = "https://www.biomedical-challenges.org/submission-system/auth/confirmation"
        email_confirmation_url_with_token = f"{email_confirmation_url}?code={user.email_confirmation_token}"

        # Prepare the email schema with all the required template variables.
        email_schema = EmailSchema(
            recipients=recipients,
            subject="Confirm your e-mail address on biomedical-challenges.org",
            template_body={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email_confirmation_token": user.email_confirmation_token,
                "email_confirmation_url": email_confirmation_url,
                "email_confirmation_url_with_token": email_confirmation_url_with_token,
            },
        )

        # Add the email sending function to the background tasks.

        if settings.environment != "dev":
            # * Add to background tasks
            self.background_tasks.add_task(
                email_sender,  # Your function that sends the email
                email=email_schema,
                template_name="email_confirmation.html",
            )
            logger.info(f"E-mail scheduled to {email_schema.recipients}")
        else:
            logger.debug("E-mail scheduled:")
            logger.debug(email_schema)

    def schedule_email_reset_password(self, user: UserModel) -> None:
        """
        Prepares and schedules the email reset token task.
        """
        # Prepare the recipient(s)
        recipients = user.email
        if recipients and not isinstance(recipients, list) and isinstance(recipients, str):
            recipients = [recipients]

        # Build the variables for e-mail template.
        reset_password_url = "https://www.biomedical-challenges.org/submission-system/auth/reset-password"
        reset_password_url_with_token = f"{reset_password_url}?token={user.reset_token}"

        # Prepare the email schema with all the required template variables.
        email_schema = EmailSchema(
            recipients=recipients,
            subject="Your password reset request on biomedical-challenges.org",
            template_body={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "reset_token": user.reset_token,
                "reset_password_url": reset_password_url,
                "reset_password_url_with_token": reset_password_url_with_token,
            },
        )

        # Add the email sending function to the background tasks.
        if settings.environment != "dev":
            # * Add to background tasks
            self.background_tasks.add_task(
                email_sender,
                email=email_schema,
                template_name="password_reset_request.html",
            )
            logger.info(f"E-mail scheduled to {email_schema.recipients}")
        else:
            logger.debug("E-mail scheduled:")
            logger.debug(email_schema)

    def schedule_draft_submitted(
        self, recipients: List[str], submission_time: datetime, challenge_name: str, challenge_file_location
    ) -> None:
        """
        Prepares and schedules the email about challenge draft submissions to Admins and Chair.
        """
        # Prepare the recipient(s)
        if recipients and not isinstance(recipients, list) and isinstance(recipients, str):
            recipients = [recipients]
        submission_time_str = submission_time.strftime("%d/%m/%Y, %H:%M:%S") + " CET (Europe/Berlin)"

        email_schema = EmailSchema(
            recipients=recipients,
            subject=f"Proposal file for '{challenge_name}' generated",
            template_body={
                "challenge_name": challenge_name,
                "submission_time": submission_time_str,
            },
            attachments=[challenge_file_location],
        )

        # * Add to background tasks
        if settings.environment != "dev":
            # * Add to background tasks
            self.background_tasks.add_task(
                email_sender,
                email=email_schema,
                template_name="draft_submitted.html",
            )
            logger.info(f"E-mail scheduled to {email_schema.recipients}")
        else:
            logger.debug("E-mail scheduled:")
            logger.debug(email_schema)

    def schedule_own_draft_submitted(
        self,
        recipients: List[str],
        submission_time: datetime,
        first_name: str,
        last_name: str,
        challenge_name: str,
        challenge_file_location,
    ) -> None:
        """
        Prepares and schedules the email about challenge draft submissions to challenge owner.
        """
        # Prepare the recipient(s)
        if recipients and not isinstance(recipients, list) and isinstance(recipients, str):
            recipients = [recipients]
        submission_time_str = submission_time.strftime("%d/%m/%Y, %H:%M:%S") + " CET (Europe/Berlin)"

        email_schema = EmailSchema(
            recipients=recipients,
            subject="Your proposal file generated",
            template_body={
                "first_name": first_name,
                "last_name": last_name,
                "challenge_name": challenge_name,
                "submission_time": submission_time_str,
            },
            attachments=[challenge_file_location],
        )

        # * Add to background tasks

        if settings.environment != "dev":
            # * Add to background tasks
            self.background_tasks.add_task(
                email_sender,
                email=email_schema,
                template_name="own_draft_submitted.html",
            )
            logger.info(f"E-mail scheduled to {email_schema.recipients}")
        else:
            logger.debug("E-mail scheduled:")
            logger.debug(email_schema)
