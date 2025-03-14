"""check 3

Revision ID: 74516c37313c
Revises: 96881e58e252
Create Date: 2025-02-22 03:10:26.230536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74516c37313c'
down_revision: Union[str, None] = '96881e58e252'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
