"""add produto_id to avaliacoes"""

from alembic import op
import sqlalchemy as sa

revision = 'add_produto_id_to_avaliacoes'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('avaliacoes', sa.Column('produto_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_avaliacoes_produto_id', 'avaliacoes', 'produtos', ['produto_id'], ['id'], ondelete='SET NULL')

def downgrade():
    op.drop_constraint('fk_avaliacoes_produto_id', 'avaliacoes', type_='foreignkey')
    op.drop_column('avaliacoes', 'produto_id')
