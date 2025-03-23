from iam.entrypoint.common.asgi import LazyASGIApp
from iam.entrypoint.fastapi.di import container
from iam.presentation.fastapi.app import app_from


app = LazyASGIApp(app_factory=lambda: app_from(container))
