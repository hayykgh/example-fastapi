"""add users table

Revision ID: b74e12023fe1
Revises: 52ae4ab72708
Create Date: 2024-06-07 13:13:51.014996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b74e12023fe1'
down_revision: Union[str, None] = '52ae4ab72708'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users',
                    sa.Column( 'id',  sa.Integer(), nullable=False), 
                    sa.Column( 'email', sa.String(), nullable=False),
                    sa.Column( 'password', sa.String(), nullable=False),
                    sa.Column( 'created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
