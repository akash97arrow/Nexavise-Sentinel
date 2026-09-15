"""enforce user ownership on events and alerts

Revision ID: 8755876668f0
Revises: 665b5ffa6ccd
Create Date: 2026-09-15 18:37:16.050881
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8755876668f0"
down_revision: Union[str, Sequence[str], None] = "665b5ffa6ccd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

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

    op.alter_column(
        "alerts",
        "user_id",
        existing_type=sa.Integer(),
        nullable=True,
    )

    op.alter_column(
        "security_events",
        "user_id",
        existing_type=sa.Integer(),
        nullable=True,
    )