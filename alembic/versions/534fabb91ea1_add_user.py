"""Add user

Revision ID: 534fabb91ea1
Revises: 679eb3c8eda4
Create Date: 2022-11-04 22:44:27.461496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '534fabb91ea1'
down_revision = '679eb3c8eda4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass