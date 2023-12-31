"""“commit”

Revision ID: 2889d16b8217
Revises: 10d90e10626e
Create Date: 2023-10-23 16:09:56.451978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2889d16b8217'
down_revision: Union[str, None] = '10d90e10626e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('time_updated', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'time_updated')
    # ### end Alembic commands ###
