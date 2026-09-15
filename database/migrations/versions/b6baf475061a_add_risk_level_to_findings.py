from alembic import op
import sqlalchemy as sa


revision = "b6baf475061a"
down_revision = "512d12c83c2b"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "findings",
        sa.Column(
            "risk_level",
            sa.String(length=20),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column("findings", "risk_level")