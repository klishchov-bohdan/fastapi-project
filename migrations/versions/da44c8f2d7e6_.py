"""empty message

Revision ID: da44c8f2d7e6
Revises: e4d97e9e78dd
Create Date: 2023-10-23 12:43:21.760073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da44c8f2d7e6'
down_revision: Union[str, None] = 'e4d97e9e78dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
