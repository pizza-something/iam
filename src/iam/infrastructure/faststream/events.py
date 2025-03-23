from faststream.types import SendableMessage

from iam.application.ports.event_queue import AccountCreatedEvent, Event
from iam.infrastructure.pydantic.schemas.output import OutputAccountSchema


class UnhandledEventError(Exception): ...


def kafka_event_of(event: Event) -> SendableMessage:
    if isinstance(event, AccountCreatedEvent):
        return OutputAccountSchema.of(event.account)

    raise UnhandledEventError(event)
