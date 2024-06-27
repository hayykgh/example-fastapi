"""comments delete

Revision ID: ef2b06e27c48
Revises: a171317f0eca
Create Date: 2024-06-27 22:42:06.588876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef2b06e27c48'
down_revision: Union[str, None] = 'a171317f0eca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='comments_pkey'),
    sa.UniqueConstraint('email', name='comments_email_key')
    )
    # ### end Alembic commands ###
