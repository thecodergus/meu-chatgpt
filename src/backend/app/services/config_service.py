from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.config import Config
from app.services.crypto_service import encrypt_str, decrypt_str

class ConfigService:
    @staticmethod
    async def create_config(session: AsyncSession, provider: str, api_key: str) -> Config:
        """Cria uma configuração de provedor com chave criptografada"""
        encrypted = encrypt_str(api_key)
        config = Config(provider=provider, api_key_encrypted=encrypted)
        session.add(config)
        await session.commit()
        await session.refresh(config)
        return config

    @staticmethod
    async def get_api_key(session: AsyncSession, provider: str) -> Optional[str]:
        """Retorna a chave de API descriptografada para o provedor"""
        result = await session.execute(select(Config).where(Config.provider == provider).limit(1))
        config = result.scalar_one_or_none()
        if not config:
            return None
        return decrypt_str(config.api_key_encrypted)

    @staticmethod
    async def list_providers(session: AsyncSession) -> List[str]:
        """Lista todos os provedores configurados"""
        result = await session.execute(select(Config.provider))
        return [row[0] for row in result.all()]

    @staticmethod
    async def delete_config(session: AsyncSession, provider: str) -> None:
        """Remove configuração de provedor pelo nome"""
        result = await session.execute(select(Config).where(Config.provider == provider).limit(1))
        config = result.scalar_one_or_none()
        if config:
            await session.delete(config)
            await session.commit()