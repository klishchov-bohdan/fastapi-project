"""empty message

Revision ID: e8f5760397f2
Revises: 1948f621caef
Create Date: 2023-11-04 18:04:40.430054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8f5760397f2'
down_revision: Union[str, None] = '1948f621caef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('client_unique_string', sa.String(), nullable=True),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('gpt_answer', sa.String(), nullable=True),
    sa.Column('time_created', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('client_unique_string'),
    sa.UniqueConstraint('id')
    )
    op.create_unique_constraint(None, 'sessions', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'sessions', type_='unique')
    op.drop_table('chats')
    # ### end Alembic commands ###