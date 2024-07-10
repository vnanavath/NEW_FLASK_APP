"""added emp_table

Revision ID: 6bfb05f23643
Revises: fd9e8ca10762
Create Date: 2024-07-02 00:54:44.092367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bfb05f23643'
down_revision = 'fd9e8ca10762'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee',
    sa.Column('emp_id', sa.Integer(), nullable=False),
    sa.Column('emp_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('emp_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employee')
    # ### end Alembic commands ###