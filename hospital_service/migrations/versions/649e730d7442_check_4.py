"""check 4

Revision ID: 649e730d7442
Revises: 74516c37313c
Create Date: 2025-02-22 03:12:43.729809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '649e730d7442'
down_revision: Union[str, None] = '74516c37313c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
