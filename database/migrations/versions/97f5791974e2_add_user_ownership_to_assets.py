"""add user ownership to assets

Revision ID: 97f5791974e2
Revises: cc93f46b97da
Create Date: 2026-09-15 17:23:11.288344

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision: str = "97f5791974e2"
down_revision: Union[str, Sequence[str], None] = "cc93f46b97da"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "assets",
        sa.Column("user_id", sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        "fk_assets_user_id_users",
        "assets",
        "users",
        ["user_id"],
        ["id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_assets_user_id_users",
        "assets",
        type_="foreignkey"
    )

    op.drop_column("assets", "user_id")