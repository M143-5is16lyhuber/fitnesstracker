"""followers

Revision ID: 1dec6c790702
Revises: fef521a5bc47
Create Date: 2024-09-08 14:37:34.656118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1dec6c790702'
down_revision = 'fef521a5bc47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
