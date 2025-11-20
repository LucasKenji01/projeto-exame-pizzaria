"""Add imagem_url to Produto

Revision ID: add_imagem_url
Revises: 
Create Date: 2025-11-18 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_imagem_url'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add imagem_url column to produtos table
    op.add_column('produtos', sa.Column('imagem_url', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove imagem_url column from produtos table
    op.drop_column('produtos', 'imagem_url')
