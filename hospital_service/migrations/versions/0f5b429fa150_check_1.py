"""check 1

Revision ID: 0f5b429fa150
Revises: 2835f5c0cf47
Create Date: 2025-02-22 03:01:36.020213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f5b429fa150'
down_revision: Union[str, None] = '2835f5c0cf47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
