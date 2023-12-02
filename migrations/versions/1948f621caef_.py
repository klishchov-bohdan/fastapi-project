"""empty message

Revision ID: 1948f621caef
Revises: 2885f4d304a0
Create Date: 2023-11-04 18:03:22.204514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1948f621caef'
down_revision: Union[str, None] = '2885f4d304a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
