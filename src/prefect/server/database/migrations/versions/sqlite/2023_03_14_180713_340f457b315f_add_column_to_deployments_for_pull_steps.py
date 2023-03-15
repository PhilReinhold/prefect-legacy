"""Add column to deployments for pull steps

Revision ID: 340f457b315f
Revises: f3df94dca3cc
Create Date: 2023-03-14 18:07:13.733969

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite


# revision identifiers, used by Alembic.
revision = "340f457b315f"
down_revision = "f3df94dca3cc"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("PRAGMA foreign_keys=OFF")
    with op.batch_alter_table("deployment", schema=None) as batch_op:
        batch_op.add_column(sa.Column("pull_steps", sqlite.JSON(), nullable=True))
    op.execute("PRAGMA foreign_keys=ON")


def downgrade():
    op.execute("PRAGMA foreign_keys=OFF")
    with op.batch_alter_table("deployment", schema=None) as batch_op:
        batch_op.drop_column("pull_steps")
    op.execute("PRAGMA foreign_keys=ON")