from dishka import AsyncContainer
from dishka.integrations.faststream import setup_dishka
from faststream import FastStream

from iam.infrastructure.faststream.publisher_regitry import (
    KafkaPublisherRegistry,
)


async def app_from(container: AsyncContainer) -> FastStream:
    regitry = await container.get(KafkaPublisherRegistry)

    app = FastStream(regitry.broker)
    setup_dishka(container, app, auto_inject=True)

    return app
