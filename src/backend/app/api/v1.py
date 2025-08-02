from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
import time
import uuid
from typing import List
import asyncio
from ..models.openai import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionChoice,
    Message,
    Usage,
    ChatCompletionChunk,
    ChatCompletionChunkChoice,
    ChatCompletionChunkDelta
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
            
            # Processa a requisição usando LangGraph com o provedor especificado
            response_stream = langgraph_service.stream_chat_completion(
                messages,
                request.model,
                request.provider,
                request.temperature,
                request.top_p,
                request.max_tokens,
                request.functions,
                request.function_call
            )
            
            # Cria a resposta no formato OpenAI para streaming
            response_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
            created_time = int(time.time())
            
            # Processa o stream do LangGraph
            async for chunk in response_stream:
                # Converte o chunk para o formato OpenAI
                if isinstance(chunk, dict) and "messages" in chunk:
                    # Extrai o conteúdo da mensagem
                    message_content = chunk["messages"][-1].content if chunk["messages"] else ""
                    
                    # Cria um chunk no formato OpenAI
                    chat_chunk = ChatCompletionChunk(
                        id=response_id,
                        created=created_time,
                        model=request.model,
                        choices=[
                            ChatCompletionChunkChoice(
                                index=0,
                                delta=ChatCompletionChunkDelta(content=message_content),
                                finish_reason=None
                            )
                        ]
                    )
                    
                    yield f"data: {json.dumps(chat_chunk.model_dump())}\n\n"
            
            # Envia o chunk final
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            # Verifica se o erro já está formatado como resposta de erro
            if hasattr(e, 'args') and len(e.args) > 0 and isinstance(e.args[0], dict) and 'error' in e.args[0]:
                error_response = e.args[0]
                error_chunk = {
                    "error": {
                        "message": error_response['error']['message'],
                        "type": error_response['error']['type'],
                        "param": None,
                        "code": error_response['error']['type']
                    }
                }
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