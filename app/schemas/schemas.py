from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from enum import Enum

class TipoPerguntaEnum(str, Enum):
    SIM_NAO = "Sim_Não"
    MULTIPLA_ESCOLHA = "multipla_escolha"
    UNICA_ESCOLHA = "unica_escolha"
    TEXTO_LIVRE = "texto_livre"
    INTEIRO = "Inteiro"
    NUMERO_DECIMAL = "Numero com duas casa decimais"

# Schemas para OpcoesRespostas
class OpcoesRespostasBase(BaseModel):
    resposta: str
    ordem: Optional[int] = None
    resposta_aberta: bool = False

class OpcoesRespostasCreate(OpcoesRespostasBase):
    id_pergunta: int

class OpcoesRespostasUpdate(BaseModel):
    resposta: Optional[str] = None
    ordem: Optional[int] = None
    resposta_aberta: Optional[bool] = None

class OpcoesRespostasResponse(OpcoesRespostasBase):
    id: int
    id_pergunta: int
    
    model_config = ConfigDict(from_attributes=True)

# Schemas para OpcoesRespostaPergunta
class OpcoesRespostaPerguntaBase(BaseModel):
    id_opcao_resposta: int
    id_pergunta: int

class OpcoesRespostaPerguntaCreate(OpcoesRespostaPerguntaBase):
    pass

class OpcoesRespostaPerguntaResponse(OpcoesRespostaPerguntaBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Schemas para Pergunta
class PerguntaBase(BaseModel):
    titulo: str
    codigo: Optional[str] = None
    orientacao_resposta: Optional[str] = None
    ordem: Optional[int] = None
    obrigatoria: bool = False
    sub_pergunta: bool = False
    tipo_pergunta: TipoPerguntaEnum

class PerguntaCreate(PerguntaBase):
    id_formulario: int

class PerguntaUpdate(BaseModel):
    titulo: Optional[str] = None
    codigo: Optional[str] = None
    orientacao_resposta: Optional[str] = None
    ordem: Optional[int] = None
    obrigatoria: Optional[bool] = None
    sub_pergunta: Optional[bool] = None
    tipo_pergunta: Optional[TipoPerguntaEnum] = None

class PerguntaResponse(PerguntaBase):
    id: int
    id_formulario: int
    opcoes_respostas: List[OpcoesRespostasResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

# Schemas para Formulario
class FormularioBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    ordem: Optional[int] = None

class FormularioCreate(FormularioBase):
    pass

class FormularioUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    ordem: Optional[int] = None

class FormularioResponse(FormularioBase):
    id: int
    perguntas: List[PerguntaResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

# Schema para listagem simples de formulários (sem perguntas)
class FormularioSimpleResponse(FormularioBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# Schema para listagem simples de perguntas (sem opções)
class PerguntaSimpleResponse(PerguntaBase):
    id: int
    id_formulario: int
    
    model_config = ConfigDict(from_attributes=True)

# Schemas para paginação
class PaginationParams(BaseModel):
    page: int = 1
    size: int = 10

class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    size: int
    pages: int

