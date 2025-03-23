from collections.abc import Sequence

from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from iam.application.ports.map import (
    MapTo,
    NotUniqueAccountNameError,
    StoredEntityLifeCycle,
)
from iam.infrastructure.sqlalchemy.driver import (
    PostgresDriver,
    single_session_of,
)


class MapToPostgres(MapTo[Sequence[PostgresDriver]]):
    async def __call__(
        self,
        postgres_drivers: Sequence[PostgresDriver],
        effect: StoredEntityLifeCycle,
    ) -> None:
        """
        :raises iam.application.ports.map.NotUniqueAccountNameError:
        """

        session = single_session_of(postgres_drivers)

        session.add_all(effect.new_values)

        for mutated_value in effect.  mutated_values:
            await session.merge(mutated_value, load=False)

        for deleted_value in effect.deleted_values:
            await session.delete(deleted_value)

        try:
            await session.flush()
        except IntegrityError as error:
            self._handle_integrity_error(error)
            raise error from error

    def _handle_integrity_error(self, error: IntegrityError) -> None:
        if isinstance(error.orig, UniqueViolation):
            table_name = error.orig.diag.table_name
            column_name = error.orig.diag.column_name

            if table_name == "account_table" and column_name == "name_text":
                raise NotUniqueAccountNameError from error
