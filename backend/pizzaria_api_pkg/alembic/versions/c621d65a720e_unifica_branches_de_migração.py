"""unifica branches de migração

Revision ID: c621d65a720e
Revises: add_produto_id_to_avaliacoes, fix_avaliacoes_20251025_162252
Create Date: 2025-10-25 16:57:46.993225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c621d65a720e'
down_revision = ('add_produto_id_to_avaliacoes', 'fix_avaliacoes_20251025_162252')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
