import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.chat_models import init_chat_model
import logging
from .error_handler import ErrorHandler

# Configuração do logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ModelFactory:
    """Fábrica para criar modelos de linguagem com base no provedor especificado"""
    
    @staticmethod
    def initialize_model(provider: Optional[str] = None, model: str = "gpt-3.5-turbo",
                        temperature: float = 0.7, top_p: float = 1.0, max_tokens: Optional[int] = None):
        """Inicializa o modelo de linguagem com base no provedor especificado"""
        logger.debug(f"Provider recebido: {provider}")
        logger.debug(f"Modelo recebido: {model}")
        logger.debug(f"Variáveis de ambiente: {dict(os.environ)}")
        
        # Se nenhum provedor for especificado, usa as variáveis de ambiente
        if not provider:
            if os.getenv("USE_ANTHROPIC", "false").lower() == "true":
                provider = "anthropic"
            elif os.getenv("USE_OPENROUTER", "false").lower() == "true":
                provider = "openrouter"
            else:
                provider = "openai"
        
        logger.debug(f"Provider selecionado: {provider}")
        
        try:
            # Inicializa o modelo com base no provedor
            if provider.lower() == "anthropic":
                logger.debug("Inicializando modelo Anthropic")
                return ChatAnthropic(
                    model=model or "claude-3-haiku-20240307",
                    temperature=temperature,
                    top_p=top_p,
                    max_tokens=max_tokens or 1024
                )
            elif provider.lower() == "openrouter":
                # Configuração para OpenRouter
                logger.debug("Inicializando modelo OpenRouter")
                openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
                openrouter_base_url = "https://openrouter.ai/api/v1"
                
                logger.debug(f"OPENROUTER_API_KEY: {'*' * len(openrouter_api_key) if openrouter_api_key else 'NÃO ENCONTRADA'}")
                logger.debug(f"OPENROUTER_BASE_URL: {openrouter_base_url}")
                
                model_instance = init_chat_model(
                    f"openai:{model or 'gpt-3.5-turbo'}",
                    openai_api_key=openrouter_api_key,
                    openai_api_base=openrouter_base_url,
                    temperature=temperature,
                    top_p=top_p,
                    max_tokens=max_tokens
                )
                
                logger.debug(f"Modelo OpenRouter criado: {model_instance}")
                return model_instance
            else:
                # Padrão para OpenAI
                logger.debug("Inicializando modelo OpenAI")
                return init_chat_model(
                    f"openai:{model or 'gpt-3.5-turbo'}",
                    temperature=temperature,
                    top_p=top_p,
                    max_tokens=max_tokens
                )
        except Exception as e:
            # Trata erros específicos por provedor
            if provider.lower() == "anthropic":
                raise Exception(ErrorHandler.handle_anthropic_error(e))
            elif provider.lower() == "openrouter":
                raise Exception(ErrorHandler.handle_openrouter_error(e))
            elif provider.lower() == "openai":
                raise Exception(ErrorHandler.handle_openai_error(e))
            else:
                raise Exception(ErrorHandler.handle_generic_error(e, provider))