"""empty message

Revision ID: 9f9efbc85f10
Revises: 97450e14fd76
Create Date: 2018-10-08 18:34:45.991945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f9efbc85f10'
down_revision = '97450e14fd76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat', sa.Column('vars', sa.String(length=250), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chat', 'vars')
    # ### end Alembic commands ###
