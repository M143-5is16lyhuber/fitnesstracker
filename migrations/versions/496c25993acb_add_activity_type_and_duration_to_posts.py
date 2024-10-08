"""Add activity type and duration to posts

Revision ID: 496c25993acb
Revises: aaa4bed90cb1
Create Date: 2024-09-09 16:38:56.086147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '496c25993acb'
down_revision = 'aaa4bed90cb1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('activity_type', sa.String(length=64), nullable=False))
        batch_op.add_column(sa.Column('duration', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('duration')
        batch_op.drop_column('activity_type')

    # ### end Alembic commands ###
