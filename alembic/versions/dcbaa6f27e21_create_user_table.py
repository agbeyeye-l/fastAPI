"""create user table

Revision ID: dcbaa6f27e21
Revises: 
Create Date: 2021-12-06 17:32:16.818316

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcbaa6f27e21'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("user", sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("email", sa.String, nullable=False, unique=True), 
        sa.Column("password", sa.String, nullable=False),
        sa.Column("created_at",sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.sql.expression.text('now()'))
        )


def downgrade():
    op.drop_table("user")
