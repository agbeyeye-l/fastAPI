"""create post table

Revision ID: b3ce0c07590e
Revises: dcbaa6f27e21
Create Date: 2021-12-06 17:56:02.277188

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import expression


# revision identifiers, used by Alembic.
revision = 'b3ce0c07590e'
down_revision = 'dcbaa6f27e21'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("post",  sa.Column("id",sa.Integer, primary_key=True, nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("content", sa.String, nullable=False),
        sa.Column("published", sa.Boolean,server_default='True', nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.sql.expression.text('now()')),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("user.id", ondelete = "CASCADE")))


def downgrade():
    op.drop_table("post")
