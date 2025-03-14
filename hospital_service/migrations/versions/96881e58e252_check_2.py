"""check 2

Revision ID: 96881e58e252
Revises: 0f5b429fa150
Create Date: 2025-02-22 03:05:42.143941

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96881e58e252'
down_revision: Union[str, None] = '0f5b429fa150'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
