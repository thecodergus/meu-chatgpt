from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from app.db import Base
from sqlalchemy.orm import relationship

class Conversation(Base):
    __tablename__ = "conversations"

    thread_uuid = Column(String(length=36), primary_key=True, index=True)
    agent_uuid = Column(String(length=36), ForeignKey('agents.uuid'), nullable=True, index=True)
    # agent_name column removed; using only agent_uuid
    tools_enabled = Column(ARRAY(String), nullable=False, server_default="{}")
    messages = Column(JSONB(), nullable=False, server_default="[]")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    agent = relationship("Agent", back_populates="conversations")