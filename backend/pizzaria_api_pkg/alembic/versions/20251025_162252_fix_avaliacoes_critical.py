"""fix avaliacoes - adicionar FKs e constraints

Revision ID: fix_avaliacoes_20251025_162252
Revises: e36443ecee4d
Create Date: 2025-10-25 16:22:52
"""
from alembic import op
import sqlalchemy as sa

revision = 'fix_avaliacoes_20251025_162252'
down_revision = 'e36443ecee4d'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Criar tabela temporária com estrutura correta
    op.create_table('avaliacoes_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('pedido_id', sa.Integer(), nullable=False),
        sa.Column('nota', sa.Integer(), nullable=False),
        sa.Column('comentario', sa.Text(), nullable=True),
        sa.Column('data_avaliacao', sa.DateTime(), nullable=True),
        sa.CheckConstraint('nota >= 1 AND nota <= 5', name='check_nota_valida'),
        sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['pedido_id'], ['pedidos.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('cliente_id', 'pedido_id', name='uq_cliente_pedido_avaliacao')
    )
    op.create_index(op.f('ix_avaliacoes_new_id'), 'avaliacoes_new', ['id'], unique=False)

    # 2. Migrar dados existentes com segurança
    op.execute("""
        INSERT INTO avaliacoes_new (id, cliente_id, pedido_id, nota, comentario, data_avaliacao)
        SELECT
            a.id,
            c.id AS cliente_id,
            p.id AS pedido_id,
            COALESCE(a.nota, 5) AS nota,
            a.comentario,
            COALESCE(a.data, CURRENT_TIMESTAMP) AS data_avaliacao
        FROM avaliacoes a
        JOIN clientes c ON c.usuario_id = (
            SELECT id FROM usuarios WHERE nome = a.autor LIMIT 1
        )
        JOIN pedidos p ON p.cliente_id = c.id
        WHERE a.autor IS NOT NULL
          AND a.nota IS NOT NULL
          AND NOT EXISTS (
              SELECT 1 FROM avaliacoes_new an
              WHERE an.cliente_id = c.id AND an.pedido_id = p.id
          )
    """)

    # 3. Dropar tabela antiga
    op.drop_index('ix_avaliacoes_id', table_name='avaliacoes')
    op.drop_table('avaliacoes')

    # 4. Renomear tabela nova
    op.rename_table('avaliacoes_new', 'avaliacoes')


def downgrade():
    # Reverter não é trivial, apenas recria estrutura antiga
    op.create_table('avaliacoes_old',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('autor', sa.String(), nullable=False),
        sa.Column('comentario', sa.Text(), nullable=True),
        sa.Column('nota', sa.Integer(), nullable=True),
        sa.Column('data', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.execute("""
        INSERT INTO avaliacoes_old (id, autor, comentario, nota, data)
        SELECT
            a.id,
            u.nome as autor,
            a.comentario,
            a.nota,
            a.data_avaliacao
        FROM avaliacoes a
        JOIN clientes c ON c.id = a.cliente_id
        JOIN usuarios u ON u.id = c.usuario_id
    """)

    op.drop_table('avaliacoes')
    op.rename_table('avaliacoes_old', 'avaliacoes')
