"""Update user_id to int64

Revision ID: e0d427aae93e
Revises: 57bc88e06e52
Create Date: 2021-12-05 23:11:42.879573

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e0d427aae93e"
down_revision = "57bc88e06e52"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("users", "id", type_=sa.BigInteger, existing_type=sa.Integer)


def downgrade():
    op.alter_column("users", "id", type_=sa.Integer, existing_type=sa.BigInteger)
