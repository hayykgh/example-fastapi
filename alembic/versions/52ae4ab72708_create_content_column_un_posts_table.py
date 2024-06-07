"""create content column un posts table

Revision ID: 52ae4ab72708
Revises: c65b1e417374
Create Date: 2024-06-07 13:06:53.512693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52ae4ab72708'
down_revision: Union[str, None] = 'c65b1e417374'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
