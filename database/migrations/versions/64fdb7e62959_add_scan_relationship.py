"""add scan relationship

Revision ID: 64fdb7e62959
Revises: 
Create Date: 2026-09-14 03:05:17.274021

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64fdb7e62959'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "scan_results",
        sa.Column("scan_id", sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        "fk_scan_results_scan_id",
        "scan_results",
        "scans",
        ["scan_id"],
        ["id"]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "fk_scan_results_scan_id",
        "scan_results",
        type_="foreignkey"
    )

    op.drop_column("scan_results", "scan_id")
