"""changed creating and updating date users table

Revision ID: 1796f6ff5f82
Revises: 903e86f69ca3
Create Date: 2023-09-17 15:22:47.944562

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1796f6ff5f82'
down_revision: Union[str, None] = '903e86f69ca3'
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
