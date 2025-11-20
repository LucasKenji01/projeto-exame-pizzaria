"""realinhar modelos e restaurar constraints

Revision ID: realign_0001
Revises: 2856ef324a21
Create Date: 2025-10-16 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'realign_0001'
down_revision = '2856ef324a21'  # <-- importante: o ID da sua migração anterior
branch_labels = None
depends_on = None

def upgrade():
    op.create_index('ix_usuarios_id', 'usuarios', ['id'], unique=False)
    op.create_index('ix_produtos_id', 'produtos', ['id'], unique=False)
    op.create_index('ix_pedidos_id', 'pedidos', ['id'], unique=False)
    op.create_index('ix_clientes_id', 'clientes', ['id'], unique=False)
    op.create_index('ix_carrinho_id', 'carrinho', ['id'], unique=False)
    op.create_index('ix_cupons_id', 'cupons', ['id'], unique=False)

    try:
        op.create_unique_constraint('clientes_email_key', 'clientes', ['email'])
    except Exception:
        pass

    with op.batch_alter_table('cupons') as batch_op:
        batch_op.alter_column(
            'percentual_desconto',
            existing_type=sa.FLOAT(),
            nullable=False,
            server_default=sa.text('0.0')
        )

    try:
        op.create_check_constraint(
            'ck_carrinho_produto_or_personalizada_not_null',
            'carrinho',
            "(produto_id IS NOT NULL) OR (produto_personalizado_id IS NOT NULL)"
        )
    except Exception:
        pass

def downgrade():
    try:
        op.drop_constraint('ck_carrinho_produto_or_personalizada_not_null', 'carrinho', type_='check')
    except Exception:
        pass

    with op.batch_alter_table('cupons') as batch_op:
        batch_op.alter_column(
            'percentual_desconto',
            existing_type=sa.FLOAT(),
            nullable=True,
            server_default=None
        )
