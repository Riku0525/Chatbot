"""user tokens

Revision ID: 97450e14fd76
Revises: a4ed93390b19
Create Date: 2018-09-28 14:20:25.385136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97450e14fd76'
down_revision = 'a4ed93390b19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('token', sa.String(length=32), nullable=True))
    op.add_column('user', sa.Column('token_expiration', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_column('user', 'token_expiration')
    op.drop_column('user', 'token')
    # ### end Alembic commands ###