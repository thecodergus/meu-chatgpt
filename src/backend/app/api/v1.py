from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
import time
import uuid
from typing import List, Optional
from ..models.openai import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionChoice,
    Message,
    Usage
)
from ..services.langgraph_service import LangGraphService
from ..services.error_handler import ErrorHandler

from fastapi import Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.services.conversation_service import ConversationService
from pydantic import BaseModel

# Pydantic for conversation creation
class CreateConversationResponse(BaseModel):
    thread_uuid: str

# Pydantic para resposta de conversa completa
class ConversationResponse(BaseModel):
    thread_uuid: str
    agent_uuid: Optional[str]
    tools_enabled: List[str]
    messages: List[Message]

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


# Endpoint de conversas
@router.post("/conversations", response_model=CreateConversationResponse)
async def create_conversation_endpoint(
    session: AsyncSession = Depends(get_session),
    agent_uuid: Optional[str] = Body(None),
    tools_enabled: Optional[List[str]] = Body(None)
):
    conv = await ConversationService.create_conversation(session, agent_uuid, tools_enabled)
    return CreateConversationResponse(thread_uuid=conv.thread_uuid)

# Endpoints de listagem e detalhes de conversas
@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations_endpoint(
    session: AsyncSession = Depends(get_session)
):
    convs = await ConversationService.list_conversations(session)
    return [
        ConversationResponse(
            thread_uuid=c.thread_uuid,
            agent_uuid=c.agent_uuid,
            tools_enabled=c.tools_enabled,
            messages=c.messages
        )
        for c in convs
    ]

@router.get("/conversations/{thread_uuid}", response_model=ConversationResponse)
async def get_conversation_endpoint(
    thread_uuid: str,
    session: AsyncSession = Depends(get_session)
):
    conv = await ConversationService.get_conversation(session, thread_uuid)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    return ConversationResponse(
        thread_uuid=conv.thread_uuid,
        agent_uuid=conv.agent_uuid,
        tools_enabled=conv.tools_enabled,
        messages=conv.messages
    )

@router.post("/conversations/{thread_uuid}/messages", response_model=ChatCompletionResponse)
async def conversation_message_endpoint(
    thread_uuid: str,
    request: ChatCompletionRequest,
    session: AsyncSession = Depends(get_session)
):
    # Armazena mensagem do usuário
    conv = await ConversationService.append_message(session, thread_uuid, request.messages[-1].role, request.messages[-1].content)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    # Envia para LLM com histórico
    messages = conv.messages
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
    # Armazena resposta da AI
    await ConversationService.append_message(session, thread_uuid, "assistant", response_content)
    # Monta resposta OpenAI
    response_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
    created_time = int(time.time())
    prompt_tokens = sum(len(m["content"].split()) for m in messages)
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