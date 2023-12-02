"""empty message

Revision ID: 68e499046561
Revises: 987197977974
Create Date: 2023-10-14 19:34:37.483248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68e499046561'
down_revision: Union[str, None] = '987197977974'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
