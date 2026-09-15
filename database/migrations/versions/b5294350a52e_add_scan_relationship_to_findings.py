"""add scan relationship to findings

Revision ID: b5294350a52e
Revises: 64fdb7e62959
Create Date: 2026-09-14 05:57:23.179420

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5294350a52e'
down_revision: Union[str, Sequence[str], None] = '64fdb7e62959'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "findings",
        sa.Column("scan_id", sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        "fk_findings_scan_id",
        "findings",
        "scans",
        ["scan_id"],
        ["id"]
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "fk_findings_scan_id",
        "findings",
        type_="foreignkey"
    )

    op.drop_column(
        "findings",
        "scan_id"
    )