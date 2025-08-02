import pytest
from unittest.mock import MagicMock
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.services.message_converter import MessageConverter

class TestMessageConverter:
    """Testes para o MessageConverter"""
    
    def test_convert_to_langchain_messages_with_user_message(self):
        """Testa a conversão de mensagens de usuário"""
        messages = [{"role": "user", "content": "Olá, como você está?"}]
        
        result = MessageConverter.convert_to_langchain_messages(messages)
        
        assert len(result) == 1
        assert isinstance(result[0], HumanMessage)
        assert result[0].content == "Olá, como você está?"
    
    def test_convert_to_langchain_messages_with_system_message(self):
        """Testa a conversão de mensagens de sistema"""
        messages = [{"role": "system", "content": "Você é um assistente útil."}]
        
        result = MessageConverter.convert_to_langchain_messages(messages)
        
        assert len(result) == 1
        assert isinstance(result[0], SystemMessage)
        assert result[0].content == "Você é um assistente útil."
    
    def test_convert_to_langchain_messages_with_assistant_message(self):
        """Testa a conversão de mensagens do assistente"""
        messages = [{"role": "assistant", "content": "Estou bem, obrigado!"}]
        
        result = MessageConverter.convert_to_langchain_messages(messages)
        
        assert len(result) == 1
        assert isinstance(result[0], AIMessage)
        assert result[0].content == "Estou bem, obrigado!"
    
    def test_convert_to_langchain_messages_with_multiple_messages(self):
        """Testa a conversão de múltiplas mensagens"""
        messages = [
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": "Olá, como você está?"},
            {"role": "assistant", "content": "Estou bem, obrigado!"}
        ]
        
        result = MessageConverter.convert_to_langchain_messages(messages)
        
        assert len(result) == 3
        assert isinstance(result[0], SystemMessage)
        assert isinstance(result[1], HumanMessage)
        assert isinstance(result[2], AIMessage)
        assert result[0].content == "Você é um assistente útil."
        assert result[1].content == "Olá, como você está?"
        assert result[2].content == "Estou bem, obrigado!"
    
    def test_extract_assistant_response_with_assistant_message(self):
        """Testa a extração da resposta do assistente"""
        mock_message = MagicMock()
        mock_message.content = "Esta é a resposta do assistente."
        response_messages = [mock_message]
        
        result = MessageConverter.extract_assistant_response(response_messages)
        
        assert result == "Esta é a resposta do assistente."
    
    def test_extract_assistant_response_without_assistant_message(self):
        """Testa a extração da resposta do assistente quando não há mensagem do assistente"""
        # Cria uma lista vazia de mensagens
        response_messages = []
        
        result = MessageConverter.extract_assistant_response(response_messages)
        
        assert result == "Desculpe, não consegui gerar uma resposta."
    
    def test_extract_assistant_response_with_non_assistant_messages(self):
        """Testa a extração da resposta do assistente quando há apenas mensagens de outros tipos"""
        # Cria mensagens que não são do assistente
        mock_human_message = MagicMock()
        mock_system_message = MagicMock()
        response_messages = [mock_human_message, mock_system_message]
        
        result = MessageConverter.extract_assistant_response(response_messages)
        
        assert result == "Desculpe, não consegui gerar uma resposta."