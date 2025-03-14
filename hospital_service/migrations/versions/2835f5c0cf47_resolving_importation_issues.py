"""resolving importation issues

Revision ID: 2835f5c0cf47
Revises: 7ed0fe216219
Create Date: 2025-02-22 02:59:15.116187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2835f5c0cf47'
down_revision: Union[str, None] = '7ed0fe216219'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
