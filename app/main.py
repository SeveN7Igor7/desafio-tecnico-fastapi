from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.routers import formularios, perguntas, opcoes_respostas

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Formulários Dinâmicos",
    description="API para gerenciamento de formulários dinâmicos com perguntas cadastradas pelos usuários",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(formularios.router)
app.include_router(perguntas.router)
app.include_router(opcoes_respostas.router)

@app.get("/")
def read_root():
    return {
        "message": "API de Formulários Dinâmicos",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

