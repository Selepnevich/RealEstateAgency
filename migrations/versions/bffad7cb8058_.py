"""empty message

Revision ID: bffad7cb8058
Revises: d0dfbb28d910
Create Date: 2024-03-13 16:01:33.010710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bffad7cb8058'
down_revision = 'd0dfbb28d910'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Agents', schema=None) as batch_op:
        batch_op.alter_column('salary',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('Customers', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Customers', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('Agents', schema=None) as batch_op:
        batch_op.alter_column('salary',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###