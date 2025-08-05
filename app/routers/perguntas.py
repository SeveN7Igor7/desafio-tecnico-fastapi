from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func
from typing import List, Optional
from app.database.database import get_db
from app.models.models import Pergunta, Formulario
from app.schemas.schemas import (
    PerguntaCreate, 
    PerguntaUpdate, 
    PerguntaResponse, 
    PerguntaSimpleResponse,
    TipoPerguntaEnum
)

router = APIRouter(prefix="/perguntas", tags=["perguntas"])

# Schema para resposta paginada
class PerguntasPaginatedResponse:
    def __init__(self, items: List[PerguntaSimpleResponse], total: int, page: int, size: int):
        self.items = items
        self.total = total
        self.page = page
        self.size = size
        self.pages = (total + size - 1) // size

@router.post("/", response_model=PerguntaResponse, status_code=status.HTTP_201_CREATED)
def criar_pergunta(pergunta: PerguntaCreate, db: Session = Depends(get_db)):
    """Criar uma nova pergunta"""
    # Verificar se o formulário existe
    formulario = db.query(Formulario).filter(Formulario.id == pergunta.id_formulario).first()
    if not formulario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formulário não encontrado"
        )
    
    db_pergunta = Pergunta(**pergunta.model_dump())
    db.add(db_pergunta)
    db.commit()
    db.refresh(db_pergunta)
    return db_pergunta

@router.get("/", response_model=List[PerguntaSimpleResponse])
def listar_perguntas(
    formulario_id: Optional[int] = Query(None, description="Filtrar por ID do formulário"),
    tipo_pergunta: Optional[TipoPerguntaEnum] = Query(None, description="Filtrar por tipo de pergunta"),
    obrigatoria: Optional[bool] = Query(None, description="Filtrar por obrigatoriedade"),
    sub_pergunta: Optional[bool] = Query(None, description="Filtrar por sub-pergunta"),
    order_by: Optional[str] = Query("id", description="Campo para ordenação (id, titulo, ordem)"),
    order_direction: Optional[str] = Query("asc", description="Direção da ordenação (asc, desc)"),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    db: Session = Depends(get_db)
):
    """Listar perguntas com filtros, ordenação e paginação"""
    query = db.query(Pergunta)
    
    # Aplicar filtros
    if formulario_id is not None:
        query = query.filter(Pergunta.id_formulario == formulario_id)
    
    if tipo_pergunta is not None:
        query = query.filter(Pergunta.tipo_pergunta == tipo_pergunta)
    
    if obrigatoria is not None:
        query = query.filter(Pergunta.obrigatoria == obrigatoria)
    
    if sub_pergunta is not None:
        query = query.filter(Pergunta.sub_pergunta == sub_pergunta)
    
    # Aplicar ordenação
    if order_by in ["id", "titulo", "ordem"]:
        order_column = getattr(Pergunta, order_by)
        if order_direction.lower() == "desc":
            query = query.order_by(desc(order_column))
        else:
            query = query.order_by(asc(order_column))
    
    # Aplicar paginação
    offset = (page - 1) * size
    perguntas = query.offset(offset).limit(size).all()
    
    return perguntas

@router.get("/paginated", response_model=dict)
def listar_perguntas_paginado(
    formulario_id: Optional[int] = Query(None, description="Filtrar por ID do formulário"),
    tipo_pergunta: Optional[TipoPerguntaEnum] = Query(None, description="Filtrar por tipo de pergunta"),
    obrigatoria: Optional[bool] = Query(None, description="Filtrar por obrigatoriedade"),
    sub_pergunta: Optional[bool] = Query(None, description="Filtrar por sub-pergunta"),
    order_by: Optional[str] = Query("id", description="Campo para ordenação (id, titulo, ordem)"),
    order_direction: Optional[str] = Query("asc", description="Direção da ordenação (asc, desc)"),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    db: Session = Depends(get_db)
):
    """Listar perguntas com filtros, ordenação e paginação - resposta detalhada"""
    query = db.query(Pergunta)
    
    # Aplicar filtros
    if formulario_id is not None:
        query = query.filter(Pergunta.id_formulario == formulario_id)
    
    if tipo_pergunta is not None:
        query = query.filter(Pergunta.tipo_pergunta == tipo_pergunta)
    
    if obrigatoria is not None:
        query = query.filter(Pergunta.obrigatoria == obrigatoria)
    
    if sub_pergunta is not None:
        query = query.filter(Pergunta.sub_pergunta == sub_pergunta)
    
    # Contar total de registros
    total = query.count()
    
    # Aplicar ordenação
    if order_by in ["id", "titulo", "ordem"]:
        order_column = getattr(Pergunta, order_by)
        if order_direction.lower() == "desc":
            query = query.order_by(desc(order_column))
        else:
            query = query.order_by(asc(order_column))
    
    # Aplicar paginação
    offset = (page - 1) * size
    perguntas = query.offset(offset).limit(size).all()
    
    # Calcular número total de páginas
    pages = (total + size - 1) // size
    
    return {
        "items": perguntas,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
        "has_next": page < pages,
        "has_prev": page > 1
    }

@router.get("/{pergunta_id}", response_model=PerguntaResponse)
def obter_pergunta(pergunta_id: int, db: Session = Depends(get_db)):
    """Obter uma pergunta específica por ID"""
    pergunta = db.query(Pergunta).filter(Pergunta.id == pergunta_id).first()
    if not pergunta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pergunta não encontrada"
        )
    return pergunta

@router.put("/{pergunta_id}", response_model=PerguntaResponse)
def atualizar_pergunta(
    pergunta_id: int, 
    pergunta_update: PerguntaUpdate, 
    db: Session = Depends(get_db)
):
    """Atualizar uma pergunta existente"""
    pergunta = db.query(Pergunta).filter(Pergunta.id == pergunta_id).first()
    if not pergunta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pergunta não encontrada"
        )
    
    update_data = pergunta_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pergunta, field, value)
    
    db.commit()
    db.refresh(pergunta)
    return pergunta

@router.delete("/{pergunta_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_pergunta(pergunta_id: int, db: Session = Depends(get_db)):
    """Deletar uma pergunta"""
    pergunta = db.query(Pergunta).filter(Pergunta.id == pergunta_id).first()
    if not pergunta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pergunta não encontrada"
        )
    
    db.delete(pergunta)
    db.commit()
    return None

@router.get("/formulario/{formulario_id}", response_model=List[PerguntaResponse])
def listar_perguntas_formulario(
    formulario_id: int,
    tipo_pergunta: Optional[TipoPerguntaEnum] = Query(None, description="Filtrar por tipo de pergunta"),
    obrigatoria: Optional[bool] = Query(None, description="Filtrar por obrigatoriedade"),
    sub_pergunta: Optional[bool] = Query(None, description="Filtrar por sub-pergunta"),
    order_by: Optional[str] = Query("ordem", description="Campo para ordenação (id, titulo, ordem)"),
    order_direction: Optional[str] = Query("asc", description="Direção da ordenação (asc, desc)"),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    db: Session = Depends(get_db)
):
    """Listar perguntas de um formulário específico com filtros, ordenação e paginação"""
    # Verificar se o formulário existe
    formulario = db.query(Formulario).filter(Formulario.id == formulario_id).first()
    if not formulario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formulário não encontrado"
        )
    
    query = db.query(Pergunta).filter(Pergunta.id_formulario == formulario_id)
    
    # Aplicar filtros
    if tipo_pergunta is not None:
        query = query.filter(Pergunta.tipo_pergunta == tipo_pergunta)
    
    if obrigatoria is not None:
        query = query.filter(Pergunta.obrigatoria == obrigatoria)
    
    if sub_pergunta is not None:
        query = query.filter(Pergunta.sub_pergunta == sub_pergunta)
    
    # Aplicar ordenação
    if order_by in ["id", "titulo", "ordem"]:
        order_column = getattr(Pergunta, order_by)
        if order_direction.lower() == "desc":
            query = query.order_by(desc(order_column))
        else:
            query = query.order_by(asc(order_column))
    
    # Aplicar paginação
    offset = (page - 1) * size
    perguntas = query.offset(offset).limit(size).all()
    
    return perguntas



@router.get("/paginated", response_model=dict)
def listar_perguntas_paginado(
    formulario_id: Optional[int] = Query(None, description="Filtrar por ID do formulário"),
    tipo_pergunta: Optional[TipoPerguntaEnum] = Query(None, description="Filtrar por tipo de pergunta"),
    obrigatoria: Optional[bool] = Query(None, description="Filtrar por obrigatoriedade"),
    sub_pergunta: Optional[bool] = Query(None, description="Filtrar por sub-pergunta"),
    order_by: Optional[str] = Query("id", description="Campo para ordenação (id, titulo, ordem)"),
    order_direction: Optional[str] = Query("asc", description="Direção da ordenação (asc, desc)"),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    db: Session = Depends(get_db)
):
    """Listar perguntas com filtros, ordenação e paginação - resposta detalhada"""
    query = db.query(Pergunta)
    
    # Aplicar filtros
    if formulario_id is not None:
        query = query.filter(Pergunta.id_formulario == formulario_id)
    
    if tipo_pergunta is not None:
        query = query.filter(Pergunta.tipo_pergunta == tipo_pergunta)
    
    if obrigatoria is not None:
        query = query.filter(Pergunta.obrigatoria == obrigatoria)
    
    if sub_pergunta is not None:
        query = query.filter(Pergunta.sub_pergunta == sub_pergunta)
    
    # Contar total de registros
    total = query.count()
    
    # Aplicar ordenação
    if order_by in ["id", "titulo", "ordem"]:
        order_column = getattr(Pergunta, order_by)
        if order_direction.lower() == "desc":
            query = query.order_by(desc(order_column))
        else:
            query = query.order_by(asc(order_column))
    
    # Aplicar paginação
    offset = (page - 1) * size
    perguntas = query.offset(offset).limit(size).all()
    
    # Calcular número total de páginas
    pages = (total + size - 1) // size
    
    return {
        "items": perguntas,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
        "has_next": page < pages,
        "has_prev": page > 1
    }

