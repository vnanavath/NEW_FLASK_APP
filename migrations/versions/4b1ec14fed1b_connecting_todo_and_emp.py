"""connecting_todo_and_emp

Revision ID: 4b1ec14fed1b
Revises: 8ff54ff5c30e
Create Date: 2024-07-02 14:30:34.447862

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4b1ec14fed1b'
down_revision = '8ff54ff5c30e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('projects')
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('employee_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'employee', ['employee_id'], ['emp_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('employee_id')

    op.create_table('projects',
    sa.Column('proj_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('proj_name', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('employee_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.emp_id'], name='projects_ibfk_1'),
    sa.PrimaryKeyConstraint('proj_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
