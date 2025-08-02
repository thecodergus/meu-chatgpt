import logging
from typing import Any, Dict, Optional

# Configuração do logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ErrorHandler:
    """Manipulador de erros específico por provedor"""
    
    @staticmethod
    def handle_openai_error(error: Exception) -> Dict[str, Any]:
        """Trata erros específicos do OpenAI"""
        logger.error(f"Erro no provedor OpenAI: {error}")
        return {
            "error": {
                "message": "Erro ao processar a requisição com o provedor OpenAI",
                "type": "openai_error",
                "details": str(error)
            }
        }
    
    @staticmethod
    def handle_anthropic_error(error: Exception) -> Dict[str, Any]:
        """Trata erros específicos do Anthropic"""
        logger.error(f"Erro no provedor Anthropic: {error}")
        return {
            "error": {
                "message": "Erro ao processar a requisição com o provedor Anthropic",
                "type": "anthropic_error",
                "details": str(error)
            }
        }
    
    @staticmethod
    def handle_openrouter_error(error: Exception) -> Dict[str, Any]:
        """Trata erros específicos do OpenRouter"""
        logger.error(f"Erro no provedor OpenRouter: {error}")
        return {
            "error": {
                "message": "Erro ao processar a requisição com o provedor OpenRouter",
                "type": "openrouter_error",
                "details": str(error)
            }
        }
    
    @staticmethod
    def handle_generic_error(error: Exception, provider: Optional[str] = None) -> Dict[str, Any]:
        """Trata erros genéricos"""
        logger.error(f"Erro genérico{' no provedor ' + provider if provider else ''}: {error}")
        return {
            "error": {
                "message": f"Erro ao processar a requisição{' com o provedor ' + provider if provider else ''}",
                "type": "generic_error",
                "details": str(error)
            }
        }