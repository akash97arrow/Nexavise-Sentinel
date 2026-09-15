"""remove scan id from findings

Revision ID: b93b52cac923
Revises: b5294350a52e
Create Date: 2026-09-14 06:25:07.836621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b93b52cac923'
down_revision: Union[str, Sequence[str], None] = 'b5294350a52e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.drop_constraint(
        "fk_findings_scan_id",
        "findings",
        type_="foreignkey"
    )

    op.drop_column(
        "findings",
        "scan_id"
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.add_column(
        "findings",
        sa.Column(
            "scan_id",
            sa.Integer(),
            nullable=True
        )
    )

    op.create_foreign_key(
        "fk_findings_scan_id",
        "findings",
        "scans",
        ["scan_id"],
        ["id"]
    )