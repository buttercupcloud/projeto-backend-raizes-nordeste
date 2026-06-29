from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from domain import models, schemas
from datetime import datetime

router = APIRouter()

@router.post("/pagamentos/mock")
def processar_pagamento_mock(pagamento: schemas.PagamentoMock, db: Session = Depends(get_db)):
    
    # 1. Procura a comanda do cliente no banco
    pedido = db.query(models.Pedido).filter(models.Pedido.id_pedido == pagamento.id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    if pedido.status != 'RECEBIDO':
        raise HTTPException(status_code=400, detail="Este pedido já foi pago ou cancelado.")

    # 2. Cria o comprovante de pagamento APROVADO
    novo_pagamento = models.Pagamento(
        id_pedido=pagamento.id_pedido,
        status='APROVADO',
        forma_pagamento=pagamento.forma_pagamento,
        processado_em=datetime.now()
    )
    db.add(novo_pagamento)

    # 3. Muda o status do Pedido para a cozinha começar a fazer
    pedido.status = 'EM_PREPARO'
    
    db.commit()
    db.refresh(novo_pagamento)

    return {
        "mensagem": "Pagamento aprovado com sucesso! Seu pedido está sendo preparado.",
        "id_pagamento": novo_pagamento.id_pagamento,
        "novo_status_pedido": pedido.status
    }