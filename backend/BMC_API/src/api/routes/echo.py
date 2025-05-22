from fastapi import APIRouter

from BMC_API.src.api.schemas.echo_schema import Message

router = APIRouter()


@router.post("/", response_model=Message)
async def send_echo_message(
    incoming_message: Message,
) -> Message:
    """
    Sends echo back to user.

    **Parameters:**

    * `incoming_message`: incoming message.

    **Returns:**

    * message same as the incoming.
    """
    return incoming_message
