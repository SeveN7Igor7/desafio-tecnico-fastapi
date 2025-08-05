from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.database import Base
import enum

class TipoPerguntaEnum(str, enum.Enum):
    SIM_NAO = "Sim_Não"
    MULTIPLA_ESCOLHA = "multipla_escolha"
    UNICA_ESCOLHA = "unica_escolha"
    TEXTO_LIVRE = "texto_livre"
    INTEIRO = "Inteiro"
    NUMERO_DECIMAL = "Numero com duas casa decimais"

class Formulario(Base):
    __tablename__ = "formulario"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String)
    ordem = Column(Integer)
    
    # Relacionamento com perguntas
    perguntas = relationship("Pergunta", back_populates="formulario", cascade="all, delete-orphan")

class Pergunta(Base):
    __tablename__ = "pergunta"
    
    id = Column(Integer, primary_key=True, index=True)
    id_formulario = Column(Integer, ForeignKey("formulario.id"), nullable=False)
    titulo = Column(String, nullable=False)
    codigo = Column(String)
    orientacao_resposta = Column(String)
    ordem = Column(Integer)
    obrigatoria = Column(Boolean, default=False)
    sub_pergunta = Column(Boolean, default=False)
    tipo_pergunta = Column(Enum(TipoPerguntaEnum), nullable=False)
    
    # Relacionamentos
    formulario = relationship("Formulario", back_populates="perguntas")
    opcoes_respostas = relationship("OpcoesRespostas", back_populates="pergunta", cascade="all, delete-orphan")
    opcoes_resposta_pergunta = relationship("OpcoesRespostaPergunta", back_populates="pergunta", cascade="all, delete-orphan")

class OpcoesRespostas(Base):
    __tablename__ = "opcoes_respostas"
    
    id = Column(Integer, primary_key=True, index=True)
    id_pergunta = Column(Integer, ForeignKey("pergunta.id"), nullable=False)
    resposta = Column(String, nullable=False)
    ordem = Column(Integer)
    resposta_aberta = Column(Boolean, default=False)
    
    # Relacionamentos
    pergunta = relationship("Pergunta", back_populates="opcoes_respostas")
    opcoes_resposta_pergunta = relationship("OpcoesRespostaPergunta", back_populates="opcao_resposta", cascade="all, delete-orphan")

class OpcoesRespostaPergunta(Base):
    __tablename__ = "opcoes_resposta_pergunta"
    
    id = Column(Integer, primary_key=True, index=True)
    id_opcao_resposta = Column(Integer, ForeignKey("opcoes_respostas.id"), nullable=False)
    id_pergunta = Column(Integer, ForeignKey("pergunta.id"), nullable=False)
    
    # Relacionamentos
    opcao_resposta = relationship("OpcoesRespostas", back_populates="opcoes_resposta_pergunta")
    pergunta = relationship("Pergunta", back_populates="opcoes_resposta_pergunta")

