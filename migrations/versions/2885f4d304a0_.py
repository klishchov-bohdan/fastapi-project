"""empty message

Revision ID: 2885f4d304a0
Revises: 3d016a8946f7
Create Date: 2023-11-04 18:00:51.381845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2885f4d304a0'
down_revision: Union[str, None] = '3d016a8946f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
