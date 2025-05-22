from pathlib import Path

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from jinja2 import TemplateNotFound
from loguru import logger

from BMC_API.src.core.config.settings import settings
from BMC_API.src.infrastructure.external_services.email.schema import EmailSchema

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
    USE_CREDENTIALS=False,
    VALIDATE_CERTS=False,
)


def get_fast_mail(config) -> FastMail:
    return FastMail(config)


async def email_sender(email: EmailSchema, template_name: str) -> None:
    email_model_dict = email.model_dump()
    message = MessageSchema(
        subject=email_model_dict.get("subject"),
        recipients=email_model_dict.get("recipients"),
        reply_to=email_model_dict.get("reply_to"),
        template_body=email_model_dict.get("template_body"),
        body=email_model_dict.get("body"),
        subtype=MessageType.html,
        attachments=email_model_dict.get("attachments"),
    )

    fm = get_fast_mail(conf)

    if email_model_dict.get("sender"):
        fm.config.MAIL_FROM = email_model_dict.get("sender")

    try:
        await fm.send_message(message=message, template_name=template_name)
        logger.info("E-mail has been sent to: " + str(message.recipients))
    except TemplateNotFound as e:
        logger.error(f'Template "{e}" not found')
        raise
    except Exception as e:
        logger.error(str(e))
        raise
