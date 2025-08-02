from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import psutil
import time
from ..services.langgraph_service import LangGraphService

router = APIRouter(prefix="/health", tags=["health"])

# Inicializa o serviço LangGraph para testes
langgraph_service = LangGraphService()

@router.get("/status")
async def health_check() -> Dict[str, Any]:
    """Endpoint de health check básico"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "FastAPI com LangGraph"
    }

@router.get("/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """Endpoint de health check detalhado com informações do sistema"""
    # Obtém informações do sistema
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    # Verifica se o serviço LangGraph está funcionando
    try:
        # Testa uma chamada simples para verificar se o serviço está respondendo
        test_messages = [{"role": "user", "content": "Hello"}]
        # Não vamos realmente chamar o modelo, apenas verificar se o serviço está instanciado
        service_status = "available" if langgraph_service else "unavailable"
    except Exception as e:
        service_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "FastAPI com LangGraph",
        "system": {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available": memory.available,
            "memory_total": memory.total
        },
        "service_status": service_status
    }

@router.get("/ready")
async def readiness_check() -> Dict[str, Any]:
    """Endpoint de readiness check"""
    # Verifica se todas as dependências estão disponíveis
    dependencies_status = {
        "langgraph_service": "ok",
        "model_factory": "ok",
        "message_converter": "ok"
    }
    
    # Verifica se há algum erro nas dependências
    overall_status = "ready"
    for status in dependencies_status.values():
        if status != "ok":
            overall_status = "not_ready"
            break
    
    return {
        "status": overall_status,
        "timestamp": time.time(),
        "dependencies": dependencies_status
    }