from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, Date, Numeric, Enum
from infrastructure.database import Base

# 1. Tabela de Usuários
class Usuario(Base):
    __tablename__ = "usuario"
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)
    perfil_role = Column(String(50), nullable=False)
    consentimento = Column(Boolean, default=False)
    saldo_pontos = Column(Integer, default=0)

# 2. Tabela de Unidades
class Unidade(Base):
    __tablename__ = "unidade"
    id_unidade = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cidade = Column(String(100))
    estado = Column(String(2))
    ativa = Column(Boolean, default=True)

# 3. Tabela de Produtos
class Produto(Base):
    __tablename__ = "produto"
    id_produto = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    preco = Column(Numeric(10, 2), nullable=False)
    categoria = Column(String(50))
    ativo = Column(Boolean, default=True)

# 4. Tabela de Cardápio por Unidade
class CardapioUnidade(Base):
    __tablename__ = "cardapio_unidade"
    id_cardapio_unidade = Column(Integer, primary_key=True, autoincrement=True)
    id_unidade = Column(Integer, ForeignKey("unidade.id_unidade"))
    id_produto = Column(Integer, ForeignKey("produto.id_produto"))
    disponivel = Column(Boolean, default=True)

# 5. Tabela de Estoque
class Estoque(Base):
    __tablename__ = "estoque"
    id_estoque = Column(Integer, primary_key=True, autoincrement=True)
    id_unidade = Column(Integer, ForeignKey("unidade.id_unidade"))
    id_produto = Column(Integer, ForeignKey("produto.id_produto"))
    quantidade_disponivel = Column(Integer, default=0)

# 6. Tabela de Movimentação de Estoque
class MovimentacaoEstoque(Base):
    __tablename__ = "movimentacao_estoque"
    id_movimentacao_estoque = Column(Integer, primary_key=True, autoincrement=True)
    id_estoque = Column(Integer, ForeignKey("estoque.id_estoque"))
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    tipo = Column(Enum('ENTRADA', 'SAIDA', name="tipo_movimentacao"))
    quantidade = Column(Integer, nullable=False)
    motivo = Column(String(255))
    criado_em = Column(DateTime)

# 7. Tabela de Campanhas Promocionais
class CampanhaPromocional(Base):
    __tablename__ = "campanha_promocional"
    id_campanha = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    tipo_desconto = Column(Enum('PERCENTUAL', 'VALOR_FIXO', name="tipo_desconto"))
    valor_desconto = Column(Numeric(10, 2))
    data_inicio = Column(Date)
    ativo = Column(Boolean, default=True)

# 8. Tabela de Pedidos
class Pedido(Base):
    __tablename__ = "pedido"
    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    id_unidade = Column(Integer, ForeignKey("unidade.id_unidade"))
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    id_campanha = Column(Integer, ForeignKey("campanha_promocional.id_campanha"), nullable=True)
    
    # A regra de Ouro do manual: A multicanalidade!
    canalPedido = Column(Enum('APP', 'TOTEM', 'BALCAO', 'PICKUP', 'WEB', name="canal_pedido"), nullable=False)
    status = Column(Enum('RECEBIDO', 'EM_PREPARO', 'PRONTO', 'ENTREGUE', 'CANCELADO', name="status_pedido"))
    valor_total = Column(Numeric(10, 2))
    criado_em = Column(DateTime)

# 9. Tabela de Itens do Pedido
class ItemPedido(Base):
    __tablename__ = "item_pedido"
    id_item_pedido = Column(Integer, primary_key=True, autoincrement=True)
    id_pedido = Column(Integer, ForeignKey("pedido.id_pedido"))
    id_produto = Column(Integer, ForeignKey("produto.id_produto"))
    quantidade = Column(Integer, nullable=False) # Corrigido o pequeno erro de digitação do DER (quatidade)
    preco_unitario = Column(Numeric(10, 2))

# 10. Tabela de Pagamentos
class Pagamento(Base):
    __tablename__ = "pagamento"
    id_pagamento = Column(Integer, primary_key=True, autoincrement=True)
    id_pedido = Column(Integer, ForeignKey("pedido.id_pedido"))
    status = Column(Enum('PENDENTE', 'APROVADO', 'RECUSADO', name="status_pagamento"))
    forma_pagamento = Column(String(100))
    processado_em = Column(DateTime)

# 11. Tabela de Histórico de Fidelidade
class HistoricoFidelidade(Base):
    __tablename__ = "historico_fidelidade"
    id_historico_fidelidade = Column(Integer, primary_key=True, autoincrement=True)
    id_pedido = Column(Integer, ForeignKey("pedido.id_pedido"))
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    tipo = Column(Enum('CREDITO', 'DEBITO', name="tipo_fidelidade"))
    pontos = Column(Integer)
    criado_em = Column(DateTime)

# 12. Tabela de Log de Auditoria
class LogAuditoria(Base):
    __tablename__ = "log_auditoria"
    id_log = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    id_pedido = Column(Integer, ForeignKey("pedido.id_pedido"), nullable=True)
    acao = Column(String(100))
    detalhes = Column(Text)
    criado_em = Column(DateTime)