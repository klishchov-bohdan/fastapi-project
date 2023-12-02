"""empty message

Revision ID: e4d97e9e78dd
Revises: 68e499046561
Create Date: 2023-10-14 19:42:34.018174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4d97e9e78dd'
down_revision: Union[str, None] = '68e499046561'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
