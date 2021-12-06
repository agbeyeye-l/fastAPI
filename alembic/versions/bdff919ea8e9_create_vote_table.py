"""create vote table

Revision ID: bdff919ea8e9
Revises: b3ce0c07590e
Create Date: 2021-12-06 18:00:32.164496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdff919ea8e9'
down_revision = 'b3ce0c07590e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("vote", sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("post_id", sa.Integer, sa.ForeignKey("post.id", ondelete="CASCADE"), primary_key=True))


def downgrade():
    op.drop_table("vote")
