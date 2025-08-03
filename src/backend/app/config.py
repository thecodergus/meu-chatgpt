import os
import logging
from dotenv import load_dotenv

# Configuração do logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Carrega as variáveis de ambiente
load_dotenv()

def validate_environment_variables():
    """Valida as variáveis de ambiente obrigatórias"""
    # Verifica se pelo menos uma chave de API está definida
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    if not openai_key and not anthropic_key and not openrouter_key:
        raise ValueError(
            "Nenhuma chave de API encontrada. Defina pelo menos uma das seguintes variáveis de ambiente: "
            "OPENAI_API_KEY, ANTHROPIC_API_KEY ou OPENROUTER_API_KEY"
        )
    
    # Log das variáveis de ambiente
    logger.debug(f"OPENAI_API_KEY: {'*' * len(openai_key) if openai_key else 'NÃO ENCONTRADA'}")
    logger.debug(f"ANTHROPIC_API_KEY: {'*' * len(anthropic_key) if anthropic_key else 'NÃO ENCONTRADA'}")
    logger.debug(f"OPENROUTER_API_KEY: {'*' * len(openrouter_key) if openrouter_key else 'NÃO ENCONTRADA'}")
    logger.debug(f"USE_ANTHROPIC: {os.getenv('USE_ANTHROPIC', 'NÃO DEFINIDO')}")
    logger.debug(f"USE_OPENROUTER: {os.getenv('USE_OPENROUTER', 'NÃO DEFINIDO')}")
    
    # Verifica as variáveis de uso
    use_anthropic = os.getenv("USE_ANTHROPIC", "false").lower() == "true"
    use_openrouter = os.getenv("USE_OPENROUTER", "false").lower() == "true"
    
    # Se USE_ANTHROPIC estiver definido como true, verifica se ANTHROPIC_API_KEY está definida
    if use_anthropic and not anthropic_key:
        raise ValueError(
            "USE_ANTHROPIC está definido como true, mas ANTHROPIC_API_KEY não está definida"
        )
    
    # Se USE_OPENROUTER estiver definido como true, verifica se OPENROUTER_API_KEY está definida
    if use_openrouter and not openrouter_key:
        raise ValueError(
            "USE_OPENROUTER está definido como true, mas OPENROUTER_API_KEY não está definida"
        )
    
    return True