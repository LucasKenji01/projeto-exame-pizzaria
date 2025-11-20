from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import relationship
from pizzaria_api_pkg.database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    tipo_usuario = Column(String, nullable=False)
    cliente = relationship("Cliente", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    funcionario = relationship("Funcionario", back_populates="usuario", uselist=False, cascade="all, delete-orphan")

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False)
    telefone = Column(String)
    endereco = Column(String)
    usuario = relationship("Usuario", back_populates="cliente")
    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")
    carrinho = relationship("Carrinho", back_populates="cliente", cascade="all, delete-orphan")
    favoritos = relationship("Favorito", back_populates="cliente", cascade="all, delete-orphan")
    enderecos = relationship("Endereco", back_populates="cliente", cascade="all, delete-orphan")
    avaliacoes = relationship("Avaliacao", back_populates="cliente", cascade="all, delete-orphan")

class Funcionario(Base):
    __tablename__ = "funcionarios"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False)
    nome = Column(String, nullable=False)
    telefone = Column(String)
    email = Column(String, unique=True)
    usuario = relationship("Usuario", back_populates="funcionario")
    entregas = relationship("Entrega", back_populates="funcionario")

class CategoriaProduto(Base):
    __tablename__ = "categorias_produto"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    descricao = Column(Text)
    produtos = relationship("Produto", back_populates="categoria", cascade="all, delete-orphan")

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    descricao = Column(Text)
    preco = Column(Float, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias_produto.id"))
    ativo = Column(Boolean, default=True)
    imagem_url = Column(String, nullable=True)  # URL da imagem (ex: /assets/pizzas/pizza-1.png)
    categoria = relationship("CategoriaProduto", back_populates="produtos")
    __table_args__ = (CheckConstraint('preco > 0', name='check_preco_positivo'),)

class Ingrediente(Base):
    __tablename__ = "ingredientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False, index=True)
    preco = Column(Float, default=0.0, nullable=False)
    disponivel = Column(Boolean, default=True)
    __table_args__ = (CheckConstraint('preco >= 0', name='check_ingrediente_preco'),)

class PizzaPersonalizada(Base):
    __tablename__ = "pizza_personalizada"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco_base = Column(Float, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    ingredientes = relationship("PizzaIngrediente", back_populates="pizza_personalizada", cascade="all, delete-orphan")
    __table_args__ = (CheckConstraint('preco_base > 0', name='check_pizza_preco'),)

class PizzaIngrediente(Base):
    __tablename__ = "pizza_ingredientes"
    id = Column(Integer, primary_key=True, index=True)
    pizza_personalizada_id = Column(Integer, ForeignKey("pizza_personalizada.id", ondelete="CASCADE"))
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"))
    quantidade = Column(Integer, default=1, nullable=False)
    pizza_personalizada = relationship("PizzaPersonalizada", back_populates="ingredientes")
    ingrediente = relationship("Ingrediente")
    __table_args__ = (CheckConstraint('quantidade > 0', name='check_quantidade_positiva'),)

class Carrinho(Base):
    __tablename__ = "carrinho"
    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=True)
    produto_personalizado_id = Column(Integer, ForeignKey("pizza_personalizada.id"), nullable=True)
    quantidade = Column(Integer, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    cliente = relationship("Cliente", back_populates="carrinho")
    produto = relationship("Produto")
    produto_personalizado = relationship("PizzaPersonalizada")
    __table_args__ = (
        CheckConstraint("(produto_id IS NOT NULL) OR (produto_personalizado_id IS NOT NULL)", name="ck_carrinho_produto"),
        CheckConstraint('quantidade > 0', name='check_carrinho_quantidade'),
    )

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    quantidade = Column(Integer, nullable=False)
    valor_total = Column(Float, nullable=False)
    email = Column(String)
    data_pedido = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(String, default="Finalizado", index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    cliente = relationship("Cliente", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")
    entrega = relationship("Entrega", back_populates="pedido", uselist=False, cascade="all, delete-orphan")
    pagamento = relationship("Pagamento", back_populates="pedido", uselist=False, cascade="all, delete-orphan")
    historico_status = relationship("HistoricoStatus", back_populates="pedido", cascade="all, delete-orphan")
    __table_args__ = (
        CheckConstraint('quantidade > 0', name='check_pedido_quantidade'),
        CheckConstraint('valor_total > 0', name='check_pedido_valor'),
    )

class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"))
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=True)
    produto_personalizado_id = Column(Integer, ForeignKey("pizza_personalizada.id"), nullable=True)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    preco_total = Column(Float, nullable=False)
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto")
    produto_personalizado = relationship("PizzaPersonalizada")

class Pagamento(Base):
    __tablename__ = "pagamentos"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), unique=True)
    forma_pagamento = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    data_pagamento = Column(DateTime, nullable=True)
    status = Column(String, default="pendente")
    pedido = relationship("Pedido", back_populates="pagamento")
    __table_args__ = (CheckConstraint('valor > 0', name='check_pagamento_valor'),)

class Entrega(Base):
    __tablename__ = "entregas"
    id = Column(Integer, primary_key=True, index=True)
    endereco_entrega = Column(String, nullable=False)
    data_prevista = Column(Date)
    data_entrega = Column(DateTime)
    status = Column(String, default='pendente', index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), unique=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"))
    pedido = relationship("Pedido", back_populates="entrega")
    funcionario = relationship("Funcionario", back_populates="entregas")

class Cupom(Base):
    __tablename__ = "cupons"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False, index=True)
    percentual_desconto = Column(Float, nullable=False, default=0.0)
    validade = Column(Date)
    ativo = Column(Boolean, default=True)
    __table_args__ = (CheckConstraint('percentual_desconto >= 0 AND percentual_desconto <= 100', name='check_desconto'),)

class HistoricoStatus(Base):
    __tablename__ = "historico_status"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"))
    status = Column(String, nullable=False)
    data_status = Column(DateTime, default=datetime.utcnow)
    pedido = relationship("Pedido", back_populates="historico_status")

class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="SET NULL"), nullable=True)
    nota = Column(Integer, nullable=False)
    comentario = Column(Text)
    data_avaliacao = Column(DateTime, default=datetime.utcnow)

    cliente = relationship("Cliente", back_populates="avaliacoes")
    pedido = relationship("Pedido")
    produto = relationship("Produto")

    __table_args__ = (
        CheckConstraint('nota >= 1 AND nota <= 5', name='check_nota_valida'),
    )


# Modelos adicionais (Favorito e Endereco)
class Favorito(Base):
    __tablename__ = "produtos_favoritos"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=True)
    produto_personalizado_id = Column(Integer, ForeignKey("pizza_personalizada.id", ondelete="CASCADE"), nullable=True)
    data_adicao = Column(DateTime, default=datetime.utcnow)
    
    cliente = relationship("Cliente", back_populates="favoritos")
    produto = relationship("Produto")
    produto_personalizado = relationship("PizzaPersonalizada")
    
    __table_args__ = (
        CheckConstraint('(produto_id IS NOT NULL) OR (produto_personalizado_id IS NOT NULL)', name='ck_favorito_produto'),
    )

class Endereco(Base):
    __tablename__ = "enderecos_clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
    apelido = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    logradouro = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    complemento = Column(String)
    bairro = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    referencia = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    padrao = Column(Boolean, default=False)
    ativo = Column(Boolean, default=True)
    
    cliente = relationship("Cliente", back_populates="enderecos")
    
    @property
    def rua(self):
        return self.logradouro
    
    @rua.setter
    def rua(self, value):
        self.logradouro = value
    
    @property
    def favorito(self):
        return self.padrao
    
    @favorito.setter
    def favorito(self, value):
        self.padrao = value
