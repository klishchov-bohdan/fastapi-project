"""changed creating and updating date users table

Revision ID: 152b9e5f53b3
Revises: 2b26b997a1ea
Create Date: 2023-09-17 15:04:36.076509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '152b9e5f53b3'
down_revision: Union[str, None] = '2b26b997a1ea'
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
