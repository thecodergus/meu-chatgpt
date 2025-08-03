from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, func
from app.db import Base

class Config(Base):
    __tablename__ = "configs"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String(length=255), nullable=False)
    api_key_encrypted = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)