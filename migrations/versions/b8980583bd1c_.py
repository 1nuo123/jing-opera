"""empty message

Revision ID: b8980583bd1c
Revises: bc0089218484
Create Date: 2024-03-22 19:02:38.696068

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b8980583bd1c'
down_revision = 'bc0089218484'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('_password', sa.String(length=200), nullable=False))
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', mysql.VARCHAR(length=200), nullable=False))
        batch_op.drop_column('_password')

    # ### end Alembic commands ###
