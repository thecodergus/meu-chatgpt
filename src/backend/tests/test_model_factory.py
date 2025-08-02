import pytest
from unittest.mock import patch, MagicMock
import os
from app.services.model_factory import ModelFactory

class TestModelFactory:
    """Testes para o ModelFactory"""
    
    def test_initialize_model_with_openai_provider(self):
        """Testa a inicialização do modelo com o provedor OpenAI"""
        with patch('app.services.model_factory.init_chat_model') as mock_init:
            mock_model = MagicMock()
            mock_init.return_value = mock_model
            
            model = ModelFactory.initialize_model("openai", "gpt-3.5-turbo", 0.7, 1.0, 100)
            
            # Verifica se o método init_chat_model foi chamado corretamente
            mock_init.assert_called_once_with(
                "openai:gpt-3.5-turbo",
                temperature=0.7,
                top_p=1.0,
                max_tokens=100
            )
            assert model == mock_model
    
    def test_initialize_model_with_anthropic_provider(self):
        """Testa a inicialização do modelo com o provedor Anthropic"""
        with patch('app.services.model_factory.ChatAnthropic') as mock_anthropic:
            mock_model = MagicMock()
            mock_anthropic.return_value = mock_model
            
            # Define variáveis de ambiente para o teste
            with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
                model = ModelFactory.initialize_model("anthropic", "claude-3-haiku-20240307", 0.7, 1.0, 100)
                
                # Verifica se o método ChatAnthropic foi chamado corretamente
                mock_anthropic.assert_called_once_with(
                    model="claude-3-haiku-20240307",
                    temperature=0.7,
                    top_p=1.0,
                    max_tokens=100
                )
                assert model == mock_model
    
    def test_initialize_model_with_openrouter_provider(self):
        """Testa a inicialização do modelo com o provedor OpenRouter"""
        with patch('app.services.model_factory.init_chat_model') as mock_init:
            mock_model = MagicMock()
            mock_init.return_value = mock_model
            
            # Define variáveis de ambiente para o teste
            with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
                model = ModelFactory.initialize_model("openrouter", "gpt-3.5-turbo", 0.7, 1.0, 100)
                
                # Verifica se o método init_chat_model foi chamado corretamente
                mock_init.assert_called_once_with(
                    "openai:gpt-3.5-turbo",
                    openai_api_key="test-key",
                    openai_api_base="https://openrouter.ai/api/v1",
                    temperature=0.7,
                    top_p=1.0,
                    max_tokens=100
                )
                assert model == mock_model
    
    def test_initialize_model_with_default_provider(self):
        """Testa a inicialização do modelo com o provedor padrão (OpenAI)"""
        with patch('app.services.model_factory.init_chat_model') as mock_init:
            mock_model = MagicMock()
            mock_init.return_value = mock_model
            
            model = ModelFactory.initialize_model(None, "gpt-3.5-turbo", 0.7, 1.0, 100)
            
            # Verifica se o método init_chat_model foi chamado corretamente
            mock_init.assert_called_once_with(
                "openai:gpt-3.5-turbo",
                temperature=0.7,
                top_p=1.0,
                max_tokens=100
            )
            assert model == mock_model
    
    def test_initialize_model_with_use_anthropic_env_var(self):
        """Testa a inicialização do modelo com a variável de ambiente USE_ANTHROPIC"""
        with patch('app.services.model_factory.ChatAnthropic') as mock_anthropic:
            mock_model = MagicMock()
            mock_anthropic.return_value = mock_model
            
            # Define variáveis de ambiente para o teste
            with patch.dict(os.environ, {"USE_ANTHROPIC": "true", "ANTHROPIC_API_KEY": "test-key"}):
                model = ModelFactory.initialize_model(None, "claude-3-haiku-20240307", 0.7, 1.0, 100)
                
                # Verifica se o método ChatAnthropic foi chamado corretamente
                mock_anthropic.assert_called_once_with(
                    model="claude-3-haiku-20240307",
                    temperature=0.7,
                    top_p=1.0,
                    max_tokens=100
                )
                assert model == mock_model