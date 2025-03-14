"""after initial test

Revision ID: 7ed0fe216219
Revises: af66a3bfa3e8
Create Date: 2025-02-22 02:57:59.502698

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ed0fe216219'
down_revision: Union[str, None] = 'af66a3bfa3e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
