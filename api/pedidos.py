from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from domain import models, schemas
from datetime import datetime

router = APIRouter()

@router.post("/pedidos")
def criar_pedido(pedido: schemas.PedidoCriar, db: Session = Depends(get_db)):
    
    # 1. Regra de Ouro da Faculdade: Validar o Canal do Pedido
    canais_validos = ['APP', 'TOTEM', 'BALCAO', 'PICKUP', 'WEB']
    if pedido.canalPedido not in canais_validos:
        raise HTTPException(status_code=400, detail="Canal de pedido inválido. Use APP, TOTEM, BALCAO, PICKUP ou WEB.")

    # 2. Abrir a "comanda" vazia
    novo_pedido = models.Pedido(
        id_unidade=pedido.id_unidade,
        id_usuario=pedido.id_usuario,
        canalPedido=pedido.canalPedido,
        status='RECEBIDO', # Status inicial exigido pelo manual
        valor_total=0.0,
        criado_em=datetime.now()
    )
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido) # Pegamos o número da comanda (ID) gerado

    # 3. Adicionar os itens e calcular a conta sozinhos
    valor_total = 0.0
    for item in pedido.itens:
        # Busca o prato no banco para descobrir o preço verdadeiro
        produto = db.query(models.Produto).filter(models.Produto.id_produto == item.id_produto).first()
        
        # --- NOSSA NOVA TRAVA DE SEGURANÇA AQUI ---
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto {item.id_produto} inexistente.")
        
        # Se passar da trava, calcula o valor e adiciona na conta normalmente
        valor_total += float(produto.preco) * item.quantidade
        
        novo_item = models.ItemPedido(
            id_pedido=novo_pedido.id_pedido,
            id_produto=item.id_produto,
            quantidade=item.quantidade,
            preco_unitario=produto.preco
        )
        db.add(novo_item)
    
    # 4. Fechar a conta com o valor total e salvar
    novo_pedido.valor_total = valor_total
    db.commit()
    db.refresh(novo_pedido)

    return {
        "mensagem": "Pedido recebido com sucesso na cozinha!",
        "id_pedido": novo_pedido.id_pedido,
        "valor_total": novo_pedido.valor_total,
        "canal_utilizado": novo_pedido.canalPedido
    }