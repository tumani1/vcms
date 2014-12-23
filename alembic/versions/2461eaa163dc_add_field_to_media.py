"""Add field to media

Revision ID: 2461eaa163dc
Revises: 2edd01ae697
Create Date: 2014-12-15 21:00:49.936884

"""

# revision identifiers, used by Alembic.
revision = '2461eaa163dc'
down_revision = '2edd01ae697'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('media', sa.Column('order', sa.Integer(), nullable=False, server_default="0"))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('media', 'order')
    ### end Alembic commands ###