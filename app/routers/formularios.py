from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models.models import Formulario
from app.schemas.schemas import (
    FormularioCreate, 
    FormularioUpdate, 
    FormularioResponse, 
    FormularioSimpleResponse
)

router = APIRouter(prefix="/formularios", tags=["formularios"])

@router.post("/", response_model=FormularioResponse, status_code=status.HTTP_201_CREATED)
def criar_formulario(formulario: FormularioCreate, db: Session = Depends(get_db)):
    """Criar um novo formulário"""
    db_formulario = Formulario(**formulario.model_dump())
    db.add(db_formulario)
    db.commit()
    db.refresh(db_formulario)
    return db_formulario

@router.get("/", response_model=List[FormularioSimpleResponse])
def listar_formularios(db: Session = Depends(get_db)):
    """Listar todos os formulários"""
    formularios = db.query(Formulario).all()
    return formularios

@router.get("/{formulario_id}", response_model=FormularioResponse)
def obter_formulario(formulario_id: int, db: Session = Depends(get_db)):
    """Obter um formulário específico por ID"""
    formulario = db.query(Formulario).filter(Formulario.id == formulario_id).first()
    if not formulario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formulário não encontrado"
        )
    return formulario

@router.put("/{formulario_id}", response_model=FormularioResponse)
def atualizar_formulario(
    formulario_id: int, 
    formulario_update: FormularioUpdate, 
    db: Session = Depends(get_db)
):
    """Atualizar um formulário existente"""
    formulario = db.query(Formulario).filter(Formulario.id == formulario_id).first()
    if not formulario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formulário não encontrado"
        )
    
    update_data = formulario_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(formulario, field, value)
    
    db.commit()
    db.refresh(formulario)
    return formulario

@router.delete("/{formulario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_formulario(formulario_id: int, db: Session = Depends(get_db)):
    """Deletar um formulário"""
    formulario = db.query(Formulario).filter(Formulario.id == formulario_id).first()
    if not formulario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formulário não encontrado"
        )
    
    db.delete(formulario)
    db.commit()
    return None

