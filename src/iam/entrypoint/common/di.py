from collections.abc import AsyncIterator

from dishka import AnyOf, Provider, Scope, provide
from faststream.kafka import KafkaBroker
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from iam.application.extend_session import ExtendSession
from iam.application.ports.accounts import Accounts
from iam.application.ports.clock import Clock
from iam.application.ports.event_queue import EventQueue
from iam.application.ports.expiring_token_encoding import ExpiringTokenEncoding
from iam.application.ports.map import MapTo
from iam.application.ports.transaction import TransactionOf
from iam.application.sign_in import SignIn
from iam.application.sign_up import SignUp
from iam.entities.access.password import PasswordHashing
from iam.entities.access.token import AccessToken, RefreshToken
from iam.infrastructure.adapters.accounts import InPostgresAccounts
from iam.infrastructure.adapters.clock import LocalHostClock
from iam.infrastructure.adapters.event_queue import KafkaEventQueue
from iam.infrastructure.adapters.expiring_token_encoding import (
    AccessTokenEncodingToHS256JWT,
    RefreshTokenEncodingToHS256JWT,
)
from iam.infrastructure.adapters.map import MapToPostgres
from iam.infrastructure.adapters.password_hashing import BcryptPasswordHashing
from iam.infrastructure.adapters.transaction import (
    InPostgresTransactionOf,
)
from iam.infrastructure.faststream.publisher_regitry import (
    KafkaPublisherRegistry,
)
from iam.infrastructure.typenv.envs import RuntimeEnvs
from iam.infrastructure.types import JWT


type PostgresEngine = AsyncEngine
type PostgresSession = AsyncSession


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    provide_runtime_envs = provide(source=RuntimeEnvs.load, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def provide_postgres_engine(
        self, envs: RuntimeEnvs
    ) -> PostgresEngine:
        return create_async_engine(envs.postgres_url)

    @provide(scope=Scope.APP)
    async def provide_kafka_broker(
        self, envs: RuntimeEnvs
    ) -> KafkaBroker:
        return KafkaBroker(envs.kafka_url)

    provide_kafka_publisher_registry = provide(
        KafkaPublisherRegistry, scope=Scope.APP
    )

    provide_event_queue = provide(
        KafkaEventQueue,
        provides=AnyOf[KafkaEventQueue, EventQueue],
        scope=Scope.APP,
    )

    @provide
    async def provide_postgres_session(
        self, engine: PostgresEngine
    ) -> AsyncIterator[PostgresSession]:
        session = AsyncSession(engine, autoflush=False, autobegin=False)
        async with session:
            yield session

    @provide(scope=Scope.APP)
    def provide_clock(self) -> AnyOf[LocalHostClock, Clock]:
        return LocalHostClock()

    @provide(scope=Scope.APP)
    def provide_access_token_encoding(
        self, envs: RuntimeEnvs
    ) -> ExpiringTokenEncoding[AccessToken, JWT]:
        return AccessTokenEncodingToHS256JWT(secret=envs.jwt_secret)

    @provide(scope=Scope.APP)
    def provide_refresh_token_encoding(
        self, envs: RuntimeEnvs
    ) -> ExpiringTokenEncoding[RefreshToken, JWT]:
        return RefreshTokenEncodingToHS256JWT(secret=envs.jwt_secret)

    @provide
    def provide_accounts(
        self, session: PostgresSession
    ) -> AnyOf[InPostgresAccounts, Accounts]:
        return InPostgresAccounts(session=session)

    @provide(scope=Scope.APP)
    def provide_in_postgres_transaction_of(
        self
    ) -> AnyOf[
        InPostgresTransactionOf,
        TransactionOf[tuple[InPostgresAccounts]],
    ]:
        return InPostgresTransactionOf()

    @provide(scope=Scope.APP)
    def provide_map_to(
        self
    ) -> AnyOf[
        MapToPostgres,
        MapTo[tuple[InPostgresAccounts]],
    ]:
        return MapToPostgres()

    @provide(scope=Scope.APP)
    def provide_password_hashing(
        self
    ) -> AnyOf[
        BcryptPasswordHashing,
        PasswordHashing,
    ]:
        return BcryptPasswordHashing()

    provide_sign_in = provide(
        SignIn[JWT, JWT, InPostgresAccounts],
        provides=SignIn[str, str],
    )

    provide_sign_up = provide(
        SignUp[JWT, JWT, InPostgresAccounts],
        provides=SignUp[str, str],
    )

    provide_extend_session = provide(
        ExtendSession[JWT, JWT],
        provides=ExtendSession[str, str],
    )
