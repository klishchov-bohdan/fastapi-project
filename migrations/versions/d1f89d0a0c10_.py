"""empty message

Revision ID: d1f89d0a0c10
Revises: ef762a1b8189
Create Date: 2023-09-23 22:58:35.915374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1f89d0a0c10'
down_revision: Union[str, None] = 'ef762a1b8189'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
