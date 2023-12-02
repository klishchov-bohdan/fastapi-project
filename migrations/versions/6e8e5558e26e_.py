"""empty message

Revision ID: 6e8e5558e26e
Revises: da44c8f2d7e6
Create Date: 2023-10-23 15:43:46.957746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e8e5558e26e'
down_revision: Union[str, None] = 'da44c8f2d7e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
