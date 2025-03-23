from abc import ABC, abstractmethod
from dataclasses import dataclass

from iam.application.ports.event_queue import Event
from iam.infrastructure.faststream.events import kafka_event_of
from iam.infrastructure.faststream.publisher_regitry import (
    KafkaPublisherRegistry,
)
from iam.infrastructure.in_memory_storage import (
    TransactionalInMemoryStorage,
)


@dataclass(kw_only=True, slots=True)
class InMemortyEventQueue(TransactionalInMemoryStorage[Event]):
    async def push(self, event: Event) -> None:
        self._storage.append(event)


class KafkaEventQueue(ABC):
    publisher_regitry: KafkaPublisherRegistry

    @abstractmethod
    async def push(self, event: Event) -> None:
        publisher = self.publisher_regitry.publisher_of(type(event))
        await publisher.publish(kafka_event_of(event))
