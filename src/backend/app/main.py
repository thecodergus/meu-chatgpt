from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1 import router as api_v1_router
from .api.health import router as health_router
import os
import logging
from dotenv import load_dotenv
from .config import validate_environment_variables

# Configuração do logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

PORTA: int = 8000

# Carrega as variáveis de ambiente
load_dotenv()

# Valida as variáveis de ambiente obrigatórias
try:
    validate_environment_variables()
except ValueError as e:
    logger.error(f"Erro na validação das variáveis de ambiente: {e}")
    raise

# Constante para a porta do servidor
app = FastAPI(
    title="FastAPI com LangGraph",
    description="Backend FastAPI com endpoint similar ao da OpenAI para LLMs usando LangGraph",
    version="1.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui o roteador da API v1
app.include_router(api_v1_router)

# Inclui o roteador de health check
app.include_router(health_router)

@app.get("/")
async def root():
    return {"message": "FastAPI com LangGraph está funcionando!"}

if __name__ == "__main__":
    import uvicorn
    load_dotenv()
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=PORTA)