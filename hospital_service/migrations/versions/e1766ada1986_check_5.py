"""check 5

Revision ID: e1766ada1986
Revises: 49b664699707
Create Date: 2025-02-22 03:24:41.210392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1766ada1986'
down_revision: Union[str, None] = '49b664699707'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
