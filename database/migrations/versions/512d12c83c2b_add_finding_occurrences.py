"""add finding occurrences

Revision ID: 512d12c83c2b
Revises: b93b52cac923
Create Date: 2026-09-14 06:40:58.692470

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '512d12c83c2b'
down_revision: Union[str, Sequence[str], None] = 'b93b52cac923'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "finding_occurrences",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("finding_id", sa.Integer(), nullable=False),
        sa.Column("scan_id", sa.Integer(), nullable=False),
        sa.Column("scan_result_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["finding_id"],
            ["findings.id"]
        ),
        sa.ForeignKeyConstraint(
            ["scan_id"],
            ["scans.id"]
        ),
        sa.ForeignKeyConstraint(
            ["scan_result_id"],
            ["scan_results.id"]
        ),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("finding_occurrences")