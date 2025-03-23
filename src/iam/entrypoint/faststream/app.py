import asyncio

from iam.entrypoint.faststream.di import container
from iam.infrastructure.faststream.app import app_from


app = asyncio.run(app_from(container))
