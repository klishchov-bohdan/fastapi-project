"""empty message

Revision ID: a9eaaddb74b2
Revises: e8a8fee62434
Create Date: 2023-10-23 15:46:32.520479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9eaaddb74b2'
down_revision: Union[str, None] = 'e8a8fee62434'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
