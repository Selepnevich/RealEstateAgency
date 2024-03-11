"""empty message

Revision ID: beef73e4cba4
Revises: 2e0bb2ed0a30
Create Date: 2024-03-11 11:21:14.864601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'beef73e4cba4'
down_revision = '2e0bb2ed0a30'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Realty', schema=None) as batch_op:
        batch_op.drop_column('name_img')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Realty', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name_img', sa.VARCHAR(length=40), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
