"""check 4

Revision ID: 49b664699707
Revises: 649e730d7442
Create Date: 2025-02-22 03:20:02.734072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49b664699707'
down_revision: Union[str, None] = '649e730d7442'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
