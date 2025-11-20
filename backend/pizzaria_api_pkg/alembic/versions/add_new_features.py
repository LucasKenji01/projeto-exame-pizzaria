"""add_favoritos_listas_rastreamento_enderecos_relatorios

Revision ID: add_new_features_001
Revises: fix_cliente_20251019_v2
Create Date: 2025-01-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'add_new_features_001'
down_revision = 'fix_cliente_20251019_v2'
branch_labels = None
depends_on = None


def upgrade():
    # ==================== FAVORITOS ====================
    op.create_table('produtos_favoritos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('produto_id', sa.Integer(), nullable=True),
        sa.Column('produto_personalizado_id', sa.Integer(), nullable=True),
        sa.Column('data_adicao', sa.DateTime(), nullable=True),
        sa.CheckConstraint('(produto_id IS NOT NULL) OR (produto_personalizado_id IS NOT NULL)', name='ck_favorito_produto'),
        sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['produto_id'], ['produtos.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['produto_personalizado_id'], ['pizza_personalizada.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_produtos_favoritos_id'), 'produtos_favoritos', ['id'], unique=False)
    
    # ==================== LISTAS DE COMPRAS ====================
    op.create_table('listas_compras',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('data_criacao', sa.DateTime(), nullable=True),
        sa.Column('ativa', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_listas_compras_id'), 'listas_compras', ['id'], unique=False)
    
    op.create_table('itens_lista_compras',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lista_id', sa.Integer(), nullable=False),
        sa.Column('produto_id', sa.Integer(), nullable=True),
        sa.Column('produto_personalizado_id', sa.Integer(), nullable=True),
        sa.Column('quantidade', sa.Integer(), nullable=False),
        sa.CheckConstraint('(produto_id IS NOT NULL) OR (produto_personalizado_id IS NOT NULL)', name='ck_item_lista_produto'),
        sa.CheckConstraint('quantidade > 0', name='check_quantidade_item_lista'),
        sa.ForeignKeyConstraint(['lista_id'], ['listas_compras.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['produto_id'], ['produtos.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['produto_personalizado_id'], ['pizza_personalizada.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_itens_lista_compras_id'), 'itens_lista_compras', ['id'], unique=False)
    
    # ==================== RASTREAMENTO ====================
    op.create_table('rastreamento_entregas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entrega_id', sa.Integer(), nullable=False),
        sa.Column('latitude_atual', sa.Float(), nullable=True),
        sa.Column('longitude_atual', sa.Float(), nullable=True),
        sa.Column('ultima_atualizacao', sa.DateTime(), nullable=True),
        sa.Column('distancia_restante_km', sa.Float(), nullable=True),
        sa.Column('tempo_estimado_minutos', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['entrega_id'], ['entregas.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('entrega_id')
    )
    op.create_index(op.f('ix_rastreamento_entregas_id'), 'rastreamento_entregas', ['id'], unique=False)
    
    op.create_table('historico_localizacao',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('rastreamento_id', sa.Integer(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('velocidade_kmh', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['rastreamento_id'], ['rastreamento_entregas.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_historico_localizacao_id'), 'historico_localizacao', ['id'], unique=False)
    op.create_index(op.f('ix_historico_localizacao_timestamp'), 'historico_localizacao', ['timestamp'], unique=False)
    
    # ==================== ENDEREÇOS ====================
    op.create_table('enderecos_clientes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('apelido', sa.String(), nullable=False),
        sa.Column('cep', sa.String(length=10), nullable=False),
        sa.Column('logradouro', sa.String(), nullable=False),
        sa.Column('numero', sa.String(), nullable=False),
        sa.Column('complemento', sa.String(), nullable=True),
        sa.Column('bairro', sa.String(), nullable=False),
        sa.Column('cidade', sa.String(), nullable=False),
        sa.Column('estado', sa.String(length=2), nullable=False),
        sa.Column('referencia', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('padrao', sa.Boolean(), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_enderecos_clientes_id'), 'enderecos_clientes', ['id'], unique=False)
    
    # ==================== RELATÓRIOS ====================
    op.create_table('relatorios_vendas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('data_inicio', sa.DateTime(), nullable=False),
        sa.Column('data_fim', sa.DateTime(), nullable=False),
        sa.Column('total_pedidos', sa.Integer(), nullable=True),
        sa.Column('total_faturamento', sa.Float(), nullable=True),
        sa.Column('ticket_medio', sa.Float(), nullable=True),
        sa.Column('produto_mais_vendido', sa.String(), nullable=True),
        sa.Column('data_geracao', sa.DateTime(), nullable=True),
        sa.Column('gerado_por', sa.Integer(), nullable=True),
        sa.CheckConstraint('total_faturamento >= 0', name='check_faturamento'),
        sa.ForeignKeyConstraint(['gerado_por'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_relatorios_vendas_id'), 'relatorios_vendas', ['id'], unique=False)
    
    op.create_table('logs_acesso',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=True),
        sa.Column('endpoint', sa.String(), nullable=False),
        sa.Column('metodo', sa.String(), nullable=False),
        sa.Column('status_code', sa.Integer(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('tempo_resposta_ms', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_logs_acesso_id'), 'logs_acesso', ['id'], unique=False)
    op.create_index(op.f('ix_logs_acesso_timestamp'), 'logs_acesso', ['timestamp'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_logs_acesso_timestamp'), table_name='logs_acesso')
    op.drop_index(op.f('ix_logs_acesso_id'), table_name='logs_acesso')
    op.drop_table('logs_acesso')
    
    op.drop_index(op.f('ix_relatorios_vendas_id'), table_name='relatorios_vendas')
    op.drop_table('relatorios_vendas')
    
    op.drop_index(op.f('ix_enderecos_clientes_id'), table_name='enderecos_clientes')
    op.drop_table('enderecos_clientes')
    
    op.drop_index(op.f('ix_historico_localizacao_timestamp'), table_name='historico_localizacao')
    op.drop_index(op.f('ix_historico_localizacao_id'), table_name='historico_localizacao')
    op.drop_table('historico_localizacao')
    
    op.drop_index(op.f('ix_rastreamento_entregas_id'), table_name='rastreamento_entregas')
    op.drop_table('rastreamento_entregas')
    
    op.drop_index(op.f('ix_itens_lista_compras_id'), table_name='itens_lista_compras')
    op.drop_table('itens_lista_compras')
    
    op.drop_index(op.f('ix_listas_compras_id'), table_name='listas_compras')
    op.drop_table('listas_compras')
    
    op.drop_index(op.f('ix_produtos_favoritos_id'), table_name='produtos_favoritos')
    op.drop_table('produtos_favoritos')
