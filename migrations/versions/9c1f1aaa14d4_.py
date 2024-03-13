"""empty message

Revision ID: 9c1f1aaa14d4
Revises: 
Create Date: 2024-03-13 09:53:49.964299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c1f1aaa14d4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Agents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fname', sa.String(length=40), nullable=False),
    sa.Column('lname', sa.String(length=40), nullable=False),
    sa.Column('email', sa.String(length=40), nullable=True),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('salary', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('Customers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fname', sa.String(length=40), nullable=False),
    sa.Column('lname', sa.String(length=40), nullable=False),
    sa.Column('email', sa.String(length=40), nullable=True),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('Operations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('operation_type', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Realty',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('object_type', sa.String(length=40), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=False),
    sa.Column('price', sa.String(length=10), nullable=False),
    sa.Column('square', sa.String(length=10), nullable=False),
    sa.Column('num_rooms', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Contract',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('realty_id', sa.Integer(), nullable=False),
    sa.Column('agent_id', sa.Integer(), nullable=False),
    sa.Column('operations_id', sa.Integer(), nullable=False),
    sa.Column('contract_start_date', sa.Date(), nullable=False),
    sa.Column('contract_end_date', sa.Date(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['Agents.id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['Customers.id'], ),
    sa.ForeignKeyConstraint(['operations_id'], ['Operations.id'], ),
    sa.ForeignKeyConstraint(['realty_id'], ['Realty.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('agent_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['Agents.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Tickets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('agent_id', sa.Integer(), nullable=False),
    sa.Column('tickets_start_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['Agents.id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['Customers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Tickets')
    op.drop_table('Profile')
    op.drop_table('Contract')
    op.drop_table('User')
    op.drop_table('Realty')
    op.drop_table('Operations')
    op.drop_table('Customers')
    op.drop_table('Agents')
    # ### end Alembic commands ###