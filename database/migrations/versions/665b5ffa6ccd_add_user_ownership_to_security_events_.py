"""add user ownership to security events and alerts

Revision ID: 665b5ffa6ccd
Revises: 97f5791974e2
Create Date: 2026-09-15 18:25:46.543333
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "665b5ffa6ccd"
down_revision: Union[str, Sequence[str], None] = "97f5791974e2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "security_events",
        sa.Column("user_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "alerts",
        sa.Column("user_id", sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        "fk_security_events_user_id_users",
        "security_events",
        "users",
        ["user_id"],
        ["id"],
    )

    op.create_foreign_key(
        "fk_alerts_user_id_users",
        "alerts",
        "users",
        ["user_id"],
        ["id"],
    )

    op.alter_column(
        "security_events",
        "user_id",
        existing_type=sa.Integer(),
        nullable=False,
    )


op.alter_column(
    "alerts",
    "user_id",
    existing_type=sa.Integer(),
    nullable=False,
)


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "fk_alerts_user_id_users",
        "alerts",
        type_="foreignkey",
    )

    op.drop_constraint(
        "fk_security_events_user_id_users",
        "security_events",
        type_="foreignkey",
    )

    op.drop_column("alerts", "user_id")
    op.drop_column("security_events", "user_id")
