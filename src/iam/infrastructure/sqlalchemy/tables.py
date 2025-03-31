from sqlalchemy import (
    Column,
    MetaData,
    String,
    Table,
    Uuid,
)


metadata = MetaData()

account_table = Table(
    "accounts",
    metadata,
    Column("id", Uuid(), primary_key=True, nullable=False),
    Column("name_text", String(), index=True, unique=True, nullable=False),
    Column("password_hash_text", String(), nullable=False),
)
