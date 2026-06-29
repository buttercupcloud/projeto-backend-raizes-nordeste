from pydantic import BaseModel

# JSON do cliente
class UsuarioCriar(BaseModel):
    nome: str
    cpf: str
    senha: str
    perfil_role: str
    consentimento: bool

from typing import List

# Molde do item que vai dentro do pedido
class ItemPedidoCriar(BaseModel):
    id_produto: int
    quantidade: int

# Molde principal do Pedido
class PedidoCriar(BaseModel):
    id_usuario: int
    id_unidade: int
    canalPedido: str # APP, TOTEM, BALCAO, PICKUP ou WEB
    itens: List[ItemPedidoCriar]

# Molde para receber a simulação do pagamento
class PagamentoMock(BaseModel):
    id_pedido: int
    forma_pagamento: str # PIX, CARTAO_CREDITO

# Pedido de Login
class LoginRequest(BaseModel):
    cpf: str
    senha: str