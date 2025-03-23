from dataclasses import dataclass, field

import typenv


@dataclass(kw_only=True, frozen=True, slots=True)
class RuntimeEnvs:
    jwt_secret: str = field(repr=False)
    postgres_url: str
    kafka_url: str

    @classmethod
    def load(cls) -> "RuntimeEnvs":
        env = typenv.Env()

        return RuntimeEnvs(
            jwt_secret=env.str("JWT_SECRET"),
            postgres_url=env.str("POSTGRES_URL"),
            kafka_url=env.str("KAFKA_URL"),
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class AlembicEnvs:
    postgres_url: str

    @classmethod
    def load(cls) -> "AlembicEnvs":
        env = typenv.Env()

        return AlembicEnvs(postgres_url=env.str("POSTGRES_URL"))


@dataclass(kw_only=True, frozen=True, slots=True)
class TestsEnvs:
    postgres_url: str
    kafka_url: str

    @classmethod
    def load(cls) -> "TestsEnvs":
        env = typenv.Env()

        return TestsEnvs(
            postgres_url=env.str("POSTGRES_URL"),
            kafka_url=env.str("KAFKA_URL"),
        )
