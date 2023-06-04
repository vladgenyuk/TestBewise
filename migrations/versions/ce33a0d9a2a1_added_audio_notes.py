"""Added audio notes

Revision ID: ce33a0d9a2a1
Revises: ab774b0a4996
Create Date: 2023-06-04 11:22:50.037549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce33a0d9a2a1'
down_revision = 'ab774b0a4996'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audio',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_table('audio')
    # ### end Alembic commands ###