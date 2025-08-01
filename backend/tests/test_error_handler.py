import pytest
from app.services.error_handler import ErrorHandler

class TestErrorHandler:
    """Testes para o ErrorHandler"""
    
    def test_handle_openai_error(self):
        """Testa o tratamento de erros do OpenAI"""
        error = Exception("Erro de API do OpenAI")
        result = ErrorHandler.handle_openai_error(error)
        
        assert "error" in result
        assert result["error"]["message"] == "Erro ao processar a requisição com o provedor OpenAI"
        assert result["error"]["type"] == "openai_error"
        assert result["error"]["details"] == "Erro de API do OpenAI"
    
    def test_handle_anthropic_error(self):
        """Testa o tratamento de erros do Anthropic"""
        error = Exception("Erro de API do Anthropic")
        result = ErrorHandler.handle_anthropic_error(error)
        
        assert "error" in result
        assert result["error"]["message"] == "Erro ao processar a requisição com o provedor Anthropic"
        assert result["error"]["type"] == "anthropic_error"
        assert result["error"]["details"] == "Erro de API do Anthropic"
    
    def test_handle_openrouter_error(self):
        """Testa o tratamento de erros do OpenRouter"""
        error = Exception("Erro de API do OpenRouter")
        result = ErrorHandler.handle_openrouter_error(error)
        
        assert "error" in result
        assert result["error"]["message"] == "Erro ao processar a requisição com o provedor OpenRouter"
        assert result["error"]["type"] == "openrouter_error"
        assert result["error"]["details"] == "Erro de API do OpenRouter"
    
    def test_handle_generic_error_without_provider(self):
        """Testa o tratamento de erros genéricos sem provedor"""
        error = Exception("Erro genérico")
        result = ErrorHandler.handle_generic_error(error)
        
        assert "error" in result
        assert result["error"]["message"] == "Erro ao processar a requisição"
        assert result["error"]["type"] == "generic_error"
        assert result["error"]["details"] == "Erro genérico"
    
    def test_handle_generic_error_with_provider(self):
        """Testa o tratamento de erros genéricos com provedor"""
        error = Exception("Erro genérico")
        result = ErrorHandler.handle_generic_error(error, "meu-provedor")
        
        assert "error" in result
        assert result["error"]["message"] == "Erro ao processar a requisição com o provedor meu-provedor"
        assert result["error"]["type"] == "generic_error"
        assert result["error"]["details"] == "Erro genérico"