from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.db import Base

class Agent(Base):
    __tablename__ = "agents"

    uuid = Column(String(length=36), primary_key=True, index=True)
    name = Column(String(length=100), nullable=False)
    description = Column(Text(), nullable=True)
    prompt = Column(Text(), nullable=True)
    image = Column(String(length=255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    conversations = relationship("Conversation", back_populates="agent")