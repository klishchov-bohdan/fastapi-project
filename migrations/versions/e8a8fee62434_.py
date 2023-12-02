"""empty message

Revision ID: e8a8fee62434
Revises: 6e8e5558e26e
Create Date: 2023-10-23 15:44:48.523451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8a8fee62434'
down_revision: Union[str, None] = '6e8e5558e26e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
