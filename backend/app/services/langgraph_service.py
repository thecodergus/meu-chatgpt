import uuid
from typing import List, Dict, Optional
from .model_factory import ModelFactory
from .message_converter import MessageConverter
from .graph_manager import GraphManager
import logging

# Configuração do logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class LangGraphService:
    def __init__(self):
        self.model_factory = ModelFactory()
        self.message_converter = MessageConverter()
        self.graph_manager = GraphManager()
        
    def process_chat_completion(self, messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo",
                               provider: Optional[str] = None, temperature: float = 0.7,
                               top_p: float = 1.0, max_tokens: Optional[int] = None,
                               functions: Optional[List[Dict]] = None, function_call: Optional[Union[str, Dict[str, str]]] = None):
        """Processa uma requisição de chat completion usando LangGraph"""
        try:
            # Inicializa o modelo com o provedor especificado
            model_instance = self.model_factory.initialize_model(provider, model, temperature, top_p, max_tokens)
            
            # Converte as mensagens para o formato do LangChain
            langchain_messages = self.message_converter.convert_to_langchain_messages(messages)
            
            # Processa as mensagens usando o grafo
            response = self.graph_manager.process_messages(model_instance, langchain_messages)
            
            # Extrai a última mensagem (resposta do assistente)
            return self.message_converter.extract_assistant_response(response["messages"])
        except Exception as e:
            # Trata erros específicos por provedor
            logger.error(f"Erro ao processar chat completion: {e}")
            raise
    
    def stream_chat_completion(self, messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo",
                               provider: Optional[str] = None, temperature: float = 0.7,
                               top_p: float = 1.0, max_tokens: Optional[int] = None,
                               functions: Optional[List[Dict]] = None, function_call: Optional[Union[str, Dict[str, str]]] = None):
        """Processa uma requisição de chat completion usando LangGraph com streaming"""
        try:
            # Inicializa o modelo com o provedor especificado
            model_instance = self.model_factory.initialize_model(provider, model, temperature, top_p, max_tokens)
            
            # Converte as mensagens para o formato do LangChain
            langchain_messages = self.message_converter.convert_to_langchain_messages(messages)
            
            # Processa as mensagens usando o grafo com streaming
            response = self.graph_manager.stream_messages(model_instance, langchain_messages)
            
            # Retorna o gerador de streaming
            return response
        except Exception as e:
            # Trata erros específicos por provedor
            logger.error(f"Erro ao processar chat completion com streaming: {e}")
            raise