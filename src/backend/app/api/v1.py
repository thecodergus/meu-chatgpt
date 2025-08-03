from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
import time
import uuid
from typing import List
from ..models.openai import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionChoice,
    Message,
    Usage
)
from ..services.langgraph_service import LangGraphService
from ..services.error_handler import ErrorHandler

router = APIRouter(prefix="/v1")

# Inicializa o serviço LangGraph
langgraph_service = LangGraphService()

@router.post("/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    """Endpoint similar ao da OpenAI para chat completions"""
    try:
        # Converte as mensagens para o formato esperado pelo LangGraph
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Processa a requisição usando LangGraph com o provedor especificado
        response_content = langgraph_service.process_chat_completion(
            messages,
            request.model,
            request.provider,
            request.temperature,
            request.top_p,
            request.max_tokens,
            request.functions,
            request.function_call
        )
        
        # Cria a resposta no formato OpenAI
        response_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
        created_time = int(time.time())
        
        # Calcula tokens (valores aproximados)
        prompt_tokens = sum(len(msg.content.split()) for msg in request.messages)
        completion_tokens = len(response_content.split())
        total_tokens = prompt_tokens + completion_tokens
        
        choice = ChatCompletionChoice(
            index=0,
            message=Message(role="assistant", content=response_content),
            finish_reason="stop"
        )
        
        usage = Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens
        )
        
        response = ChatCompletionResponse(
            id=response_id,
            created=created_time,
            model=request.model,
            choices=[choice],
            usage=usage
        )
        
        return response
        
    except Exception as e:
        # Verifica se o erro já está formatado como resposta de erro
        if hasattr(e, 'args') and len(e.args) > 0 and isinstance(e.args[0], dict) and 'error' in e.args[0]:
            error_response = e.args[0]
            raise HTTPException(
                status_code=500,
                detail=error_response['error']['message']
            )
        else:
            raise HTTPException(status_code=500, detail=f"Erro ao processar a requisição: {str(e)}")

@router.post("/chat/completions/stream")
async def chat_completions_stream(request: ChatCompletionRequest):
    """Endpoint para streaming de chat completions"""
    async def generate_stream():
        try:
            # Converte as mensagens para o formato esperado pelo LangGraph
            messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
            
            # Processa a requisição usando LangGraph (mockável para testes)
            response_content = langgraph_service.process_chat_completion(
                messages,
                request.model,
                request.provider,
                request.temperature,
                request.top_p,
                request.max_tokens,
                request.functions,
                request.function_call
            )
            
            # Envia o conteúdo como um único evento
            yield f"data: {response_content}\n\n"
            # Evento final
            yield "data: [DONE]\n\n"
        except Exception as e:
            # Trata erros específicos
            if hasattr(e, 'args') and len(e.args) > 0 and isinstance(e.args[0], dict) and 'error' in e.args[0]:
                error_response = e.args[0]
                error_chunk = {"error": error_response['error']}
            else:
                error_chunk = {
                    "error": {
                        "message": f"Erro ao processar a requisição: {str(e)}",
                        "type": "server_error",
                        "param": None,
                        "code": "server_error"
                    }
                }
            yield f"data: {json.dumps(error_chunk)}\n\n"
    return StreamingResponse(generate_stream(), media_type="text/event-stream")