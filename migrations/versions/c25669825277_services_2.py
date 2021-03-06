"""services 2

Revision ID: c25669825277
Revises: 9f9efbc85f10
Create Date: 2018-10-12 15:14:21.385007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c25669825277'
down_revision = '9f9efbc85f10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service', sa.Column('bot', sa.String(length=150), nullable=True))
    op.add_column('service', sa.Column('email', sa.String(length=150), nullable=True))
    op.add_column('service', sa.Column('status', sa.Integer(), nullable=True))
    op.add_column('service', sa.Column('var', sa.String(length=150), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('service', 'var')
    op.drop_column('service', 'status')
    op.drop_column('service', 'email')
    op.drop_column('service', 'bot')
    # ### end Alembic commands ###
