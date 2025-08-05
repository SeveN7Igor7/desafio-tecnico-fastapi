from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models.models import OpcoesRespostas, Pergunta
from app.schemas.schemas import (
    OpcoesRespostasCreate, 
    OpcoesRespostasUpdate, 
    OpcoesRespostasResponse
)

router = APIRouter(prefix="/opcoes-respostas", tags=["opcoes-respostas"])

@router.post("/", response_model=OpcoesRespostasResponse, status_code=status.HTTP_201_CREATED)
def criar_opcao_resposta(opcao: OpcoesRespostasCreate, db: Session = Depends(get_db)):
    """Criar uma nova opção de resposta"""
    # Verificar se a pergunta existe
    pergunta = db.query(Pergunta).filter(Pergunta.id == opcao.id_pergunta).first()
    if not pergunta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pergunta não encontrada"
        )
    
    db_opcao = OpcoesRespostas(**opcao.model_dump())
    db.add(db_opcao)
    db.commit()
    db.refresh(db_opcao)
    return db_opcao

@router.get("/pergunta/{pergunta_id}", response_model=List[OpcoesRespostasResponse])
def listar_opcoes_pergunta(pergunta_id: int, db: Session = Depends(get_db)):
    """Listar todas as opções de resposta de uma pergunta"""
    # Verificar se a pergunta existe
    pergunta = db.query(Pergunta).filter(Pergunta.id == pergunta_id).first()
    if not pergunta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pergunta não encontrada"
        )
    
    opcoes = db.query(OpcoesRespostas).filter(OpcoesRespostas.id_pergunta == pergunta_id).all()
    return opcoes

@router.get("/{opcao_id}", response_model=OpcoesRespostasResponse)
def obter_opcao_resposta(opcao_id: int, db: Session = Depends(get_db)):
    """Obter uma opção de resposta específica por ID"""
    opcao = db.query(OpcoesRespostas).filter(OpcoesRespostas.id == opcao_id).first()
    if not opcao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opção de resposta não encontrada"
        )
    return opcao

@router.put("/{opcao_id}", response_model=OpcoesRespostasResponse)
def atualizar_opcao_resposta(
    opcao_id: int, 
    opcao_update: OpcoesRespostasUpdate, 
    db: Session = Depends(get_db)
):
    """Atualizar uma opção de resposta existente"""
    opcao = db.query(OpcoesRespostas).filter(OpcoesRespostas.id == opcao_id).first()
    if not opcao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opção de resposta não encontrada"
        )
    
    update_data = opcao_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(opcao, field, value)
    
    db.commit()
    db.refresh(opcao)
    return opcao

@router.delete("/{opcao_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_opcao_resposta(opcao_id: int, db: Session = Depends(get_db)):
    """Deletar uma opção de resposta"""
    opcao = db.query(OpcoesRespostas).filter(OpcoesRespostas.id == opcao_id).first()
    if not opcao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opção de resposta não encontrada"
        )
    
    db.delete(opcao)
    db.commit()
    return None

