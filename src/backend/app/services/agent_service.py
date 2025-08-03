from typing import Optional, List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.agent import Agent

class AgentService:
    @staticmethod
    async def list_agents(session: AsyncSession) -> List[Agent]:
        result = await session.execute(select(Agent))
        return result.scalars().all()

    @staticmethod
    async def get_agent(session: AsyncSession, agent_uuid: str) -> Optional[Agent]:
        result = await session.execute(select(Agent).where(Agent.uuid == agent_uuid))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_agent(
        session: AsyncSession,
        name: str,
        description: Optional[str] = None,
        prompt: Optional[str] = None,
        image: Optional[str] = None
    ) -> Agent:
        agent_id = str(uuid.uuid4())
        agent = Agent(
            uuid=agent_id,
            name=name,
            description=description,
            prompt=prompt,
            image=image
        )
        session.add(agent)
        await session.commit()
        await session.refresh(agent)
        return agent

    @staticmethod
    async def update_agent(
        session: AsyncSession,
        agent_uuid: str,
        name: str,
        description: Optional[str] = None,
        prompt: Optional[str] = None,
        image: Optional[str] = None
    ) -> Agent:
        agent = await AgentService.get_agent(session, agent_uuid)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent não encontrado")
        agent.name = name
        agent.description = description
        agent.prompt = prompt
        agent.image = image
        await session.commit()
        await session.refresh(agent)
        return agent

    @staticmethod
    async def delete_agent(
        session: AsyncSession,
        agent_uuid: str
    ) -> None:
        agent = await AgentService.get_agent(session, agent_uuid)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent não encontrado")
        await session.delete(agent)
        await session.commit()