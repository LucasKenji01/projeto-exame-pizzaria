"""fix cliente id - versão corrigida

Revision ID: fix_cliente_20251019_v2
Revises: a8757478b5d9
Create Date: 2025-10-19 13:30:00
"""
from alembic import op
import sqlalchemy as sa

revision = 'fix_cliente_20251019_v2'
down_revision = 'a8757478b5d9'

def upgrade():
    # ==========================================
    # PARTE 1: CORRIGIR TABELA CLIENTES
    # ==========================================
    
    # 1. Adicionar coluna id temporária
    op.execute("""
        ALTER TABLE clientes ADD COLUMN IF NOT EXISTS id SERIAL;
    """)
    
    # 2. Remover foreign keys que dependem de clientes_pkey
    op.execute("""
        ALTER TABLE pedidos DROP CONSTRAINT IF EXISTS pedidos_cliente_id_fkey;
        ALTER TABLE pizza_personalizada DROP CONSTRAINT IF EXISTS pizza_personalizada_cliente_id_fkey;
        ALTER TABLE carrinho DROP CONSTRAINT IF EXISTS carrinho_cliente_id_fkey;
    """)
    
    # 3. Atualizar valores de cliente_id nas tabelas dependentes
    # (as tabelas já usam usuario_id, então mantemos os valores)
    op.execute("""
        -- Atualizar cliente_id para usar o novo id
        UPDATE pedidos p
        SET cliente_id = c.id
        FROM clientes c
        WHERE p.cliente_id = c.usuario_id;
        
        UPDATE pizza_personalizada pp
        SET cliente_id = c.id
        FROM clientes c
        WHERE pp.cliente_id = c.usuario_id;
        
        UPDATE carrinho car
        SET cliente_id = c.id
        FROM clientes c
        WHERE car.cliente_id = c.usuario_id;
    """)
    
    # 4. Remover constraint antiga de primary key
    op.execute("""
        ALTER TABLE clientes DROP CONSTRAINT IF EXISTS clientes_pkey CASCADE;
    """)
    
    # 5. Adicionar nova primary key na coluna id
    op.execute("""
        ALTER TABLE clientes ADD PRIMARY KEY (id);
    """)
    
    # 6. Adicionar constraint unique em usuario_id
    op.execute("""
        ALTER TABLE clientes ADD CONSTRAINT uq_clientes_usuario_id UNIQUE (usuario_id);
    """)
    
    # 7. Recriar foreign keys apontando para clientes.id
    op.execute("""
        ALTER TABLE pedidos 
        ADD CONSTRAINT pedidos_cliente_id_fkey 
        FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE;
        
        ALTER TABLE pizza_personalizada 
        ADD CONSTRAINT pizza_personalizada_cliente_id_fkey 
        FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE;
        
        ALTER TABLE carrinho 
        ADD CONSTRAINT carrinho_cliente_id_fkey 
        FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE;
    """)
    
    # ==========================================
    # PARTE 2: CORRIGIR TABELA FUNCIONARIOS
    # ==========================================
    
    # 1. Adicionar coluna id
    op.execute("""
        ALTER TABLE funcionarios ADD COLUMN IF NOT EXISTS id SERIAL;
    """)
    
    # 2. Remover foreign keys que dependem de funcionarios_pkey
    op.execute("""
        ALTER TABLE entregas DROP CONSTRAINT IF EXISTS entregas_funcionario_id_fkey;
    """)
    
    # 3. Atualizar valores nas tabelas dependentes
    op.execute("""
        UPDATE entregas e
        SET funcionario_id = f.id
        FROM funcionarios f
        WHERE e.funcionario_id = f.usuario_id;
    """)
    
    # 4. Remover constraint antiga
    op.execute("""
        ALTER TABLE funcionarios DROP CONSTRAINT IF EXISTS funcionarios_pkey CASCADE;
    """)
    
    # 5. Adicionar nova primary key
    op.execute("""
        ALTER TABLE funcionarios ADD PRIMARY KEY (id);
    """)
    
    # 6. Adicionar unique constraint em usuario_id
    op.execute("""
        ALTER TABLE funcionarios ADD CONSTRAINT uq_funcionarios_usuario_id UNIQUE (usuario_id);
    """)
    
    # 7. Recriar foreign key
    op.execute("""
        ALTER TABLE entregas 
        ADD CONSTRAINT entregas_funcionario_id_fkey 
        FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE SET NULL;
    """)
    
    # ==========================================
    # PARTE 3: CRIAR ÍNDICES
    # ==========================================
    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_clientes_id ON clientes(id);
        CREATE INDEX IF NOT EXISTS ix_clientes_usuario_id ON clientes(usuario_id);
        CREATE INDEX IF NOT EXISTS ix_funcionarios_id ON funcionarios(id);
        CREATE INDEX IF NOT EXISTS ix_funcionarios_usuario_id ON funcionarios(usuario_id);
    """)

def downgrade():
    # Reverter não é trivial, então apenas passamos
    # Em produção, faça backup antes de executar
    pass
