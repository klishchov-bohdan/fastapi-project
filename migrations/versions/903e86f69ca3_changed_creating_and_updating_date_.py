"""changed creating and updating date users table

Revision ID: 903e86f69ca3
Revises: c8bc4e174f91
Create Date: 2023-09-17 15:20:48.694984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '903e86f69ca3'
down_revision: Union[str, None] = 'c8bc4e174f91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###