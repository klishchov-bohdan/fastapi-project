"""empty message

Revision ID: 987197977974
Revises: d1f89d0a0c10
Create Date: 2023-10-13 12:49:41.586663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '987197977974'
down_revision: Union[str, None] = 'd1f89d0a0c10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
