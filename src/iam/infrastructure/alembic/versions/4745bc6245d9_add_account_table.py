"""add account table

Revision ID: 4745bc6245d9
Revises:
Create Date: 2025-03-23 16:38:39.002624

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "4745bc6245d9"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "accounts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name_text", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_accounts_name_text"), "accounts", ["name_text"], unique=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_accounts_name_text"), table_name="accounts")
    op.drop_table("accounts")
    # ### end Alembic commands ###
