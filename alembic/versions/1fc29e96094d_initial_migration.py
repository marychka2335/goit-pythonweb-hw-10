"""Init

Revision ID: 2e218a82ef9c
Revises: 
Create Date: 2025-04-13 11:41:51.413506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e218a82ef9c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('first_name', sa.String(
                        length=50), nullable=False),
                    sa.Column('last_name', sa.String(
                        length=50), nullable=False),
                    sa.Column('email', sa.String(length=100), nullable=False),
                    sa.Column('phone_number', sa.String(
                        length=20), nullable=True),
                    sa.Column('birthday', sa.Date(), nullable=False),
                    sa.Column('additional_data', sa.String(
                        length=255), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_contacts_email'),
                    'contacts', ['email'], unique=True)
    op.create_index(op.f('ix_contacts_phone_number'),
                    'contacts', ['phone_number'], unique=True)
    op.create_index('ix_full_name', 'contacts', [
                    'first_name', 'last_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_full_name', table_name='contacts')
    op.drop_index(op.f('ix_contacts_phone_number'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_email'), table_name='contacts')
    op.drop_table('contacts')
    # ### end Alembic commands ###
