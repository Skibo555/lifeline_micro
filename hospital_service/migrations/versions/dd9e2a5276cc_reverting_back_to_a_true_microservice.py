"""reverting back to a true microservice

Revision ID: dd9e2a5276cc
Revises: 05584772483a
Create Date: 2025-02-28 18:11:58.638803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd9e2a5276cc'
down_revision: Union[str, None] = '05584772483a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'hospitals', ['created_by'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'hospitals', type_='unique')
    # ### end Alembic commands ###
