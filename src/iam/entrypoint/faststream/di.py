from dishka import make_async_container

from iam.entrypoint.common.di import (
    ApplicationProvider,
)


container = make_async_container(ApplicationProvider())
