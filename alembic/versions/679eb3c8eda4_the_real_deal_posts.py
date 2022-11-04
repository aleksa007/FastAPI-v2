"""The real deal posts

Revision ID: 679eb3c8eda4
Revises: 3c001acd7156
Create Date: 2022-11-04 22:38:23.166168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '679eb3c8eda4'
down_revision = '3c001acd7156'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass

