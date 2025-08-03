from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.conversation import Conversation
import uuid
from fastapi import HTTPException

class ConversationService:
    @staticmethod
    async def create_conversation(
        session: AsyncSession, agent_uuid: Optional[str] = None, tools_enabled: Optional[List[str]] = None
    ) -> Conversation:
        default_tools: List[str] = []
        if agent_uuid:
            from app.models.agent import Agent
            result = await session.execute(select(Agent).where(Agent.uuid == agent_uuid))
            agent = result.scalar_one_or_none()
            if not agent:
                raise HTTPException(status_code=404, detail="Agent não encontrado")
            # define ferramentas default com base na configuração do agente
            from app.services.agents.agent_registry import AgentRegistry
            code_agent = AgentRegistry.get(agent.name)
            default_tools = code_agent.tools
        applied_tools = tools_enabled if tools_enabled else default_tools
        thread_id = str(uuid.uuid4())
        conv = Conversation(
            thread_uuid=thread_id,
            agent_uuid=agent_uuid,
            tools_enabled=applied_tools,
            messages=[]
        )
        session.add(conv)
        await session.commit()
        await session.refresh(conv)
        return conv

    @staticmethod
    async def get_conversation(session: AsyncSession, thread_uuid: str) -> Optional[Conversation]:
        result = await session.execute(select(Conversation).where(Conversation.thread_uuid == thread_uuid))
        return result.scalar_one_or_none()

    @staticmethod
    async def append_message(session: AsyncSession, thread_uuid: str, role: str, content: str) -> Optional[Conversation]:
        conv = await ConversationService.get_conversation(session, thread_uuid)
        if not conv:
            return None
        msgs = conv.messages or []
        msgs.append({"role": role, "content": content})
        conv.messages = msgs
        await session.commit()
        await session.refresh(conv)
        return conv

    @staticmethod
    async def list_conversations(session: AsyncSession) -> List[Conversation]:
        result = await session.execute(select(Conversation))
        return result.scalars().all()