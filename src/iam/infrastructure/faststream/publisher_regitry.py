from dataclasses import dataclass, field
from typing import Any

from faststream.kafka import KafkaBroker
from faststream.kafka.publisher.asyncapi import AsyncAPIPublisher

from iam.application.ports.event_queue import AccountCreatedEvent, Event
from iam.infrastructure.pydantic.schemas.output import OutputAccountSchema


@dataclass(kw_only=True, slots=True)
class KafkaPublisherRegistry:
    broker: KafkaBroker
    _map: dict[type[Event], AsyncAPIPublisher[Any]] = field(
        init=False, default_factory=dict
    )

    def publisher_of(self, event_type: type[Event]) -> AsyncAPIPublisher[Any]:
        return self._map[event_type]

    def __post_init__(self) -> None:
        self._map[AccountCreatedEvent] = self.broker.publisher(
            "account.created.ok",
            schema=OutputAccountSchema
        )
