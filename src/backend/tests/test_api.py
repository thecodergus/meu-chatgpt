import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json
from app.main import app

client = TestClient(app)

class TestAPI:
    """Testes de integração para a API"""
    
    def test_root_endpoint(self):
        """Testa o endpoint raiz"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "FastAPI com LangGraph está funcionando!"}
    
    def test_chat_completions_endpoint_with_valid_request(self):
        """Testa o endpoint de chat completions com uma requisição válida"""
        # Mock do serviço LangGraph
        mock_response = "Esta é uma resposta de teste."
        
        with patch('app.services.langgraph_service.LangGraphService.process_chat_completion') as mock_service:
            mock_service.return_value = mock_response
            
            request_data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": "Olá, como você está?"}
                ]
            }
            
            response = client.post("/v1/chat/completions", json=request_data)
            
            assert response.status_code == 200
            response_json = response.json()
            assert "id" in response_json
            assert "choices" in response_json
            assert len(response_json["choices"]) == 1
            assert response_json["choices"][0]["message"]["content"] == mock_response
    
    def test_chat_completions_endpoint_with_provider(self):
        """Testa o endpoint de chat completions com um provedor especificado"""
        # Mock do serviço LangGraph
        mock_response = "Esta é uma resposta de teste com provedor."
        
        with patch('app.services.langgraph_service.LangGraphService.process_chat_completion') as mock_service:
            mock_service.return_value = mock_response
            
            request_data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": "Olá, como você está?"}
                ],
                "provider": "openai"
            }
            
            response = client.post("/v1/chat/completions", json=request_data)
            
            assert response.status_code == 200
            response_json = response.json()
            assert "id" in response_json
            assert "choices" in response_json
            assert len(response_json["choices"]) == 1
            assert response_json["choices"][0]["message"]["content"] == mock_response
    
    def test_chat_completions_endpoint_with_functions(self):
        """Testa o endpoint de chat completions com funções"""
        # Mock do serviço LangGraph
        mock_response = "Esta é uma resposta de teste com funções."
        
        with patch('app.services.langgraph_service.LangGraphService.process_chat_completion') as mock_service:
            mock_service.return_value = mock_response
            
            request_data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": "Qual é a previsão do tempo?"}
                ],
                "functions": [
                    {
                        "name": "get_weather",
                        "description": "Obtém a previsão do tempo",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {"type": "string"}
                            }
                        }
                    }
                ]
            }
            
            response = client.post("/v1/chat/completions", json=request_data)
            
            assert response.status_code == 200
            response_json = response.json()
            assert "id" in response_json
            assert "choices" in response_json
            assert len(response_json["choices"]) == 1
            assert response_json["choices"][0]["message"]["content"] == mock_response
    
    def test_chat_completions_stream_endpoint_with_valid_request(self):
        """Testa o endpoint de streaming de chat completions com uma requisição válida"""
        # Mock do serviço LangGraph
        mock_response = "Esta é uma resposta de teste em streaming."
        
        with patch('app.services.langgraph_service.LangGraphService.process_chat_completion') as mock_service:
            mock_service.return_value = mock_response
            
            request_data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": "Olá, como você está?"}
                ],
                "stream": True
            }
            
            response = client.post("/v1/chat/completions/stream", json=request_data)
            
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/event-stream"
            
            # Verifica se o conteúdo é um stream válido
            content = response.content.decode()
            assert "data:" in content
            assert "[DONE]" in content
    
    def test_chat_completions_endpoint_with_invalid_request(self):
        """Testa o endpoint de chat completions com uma requisição inválida"""
        request_data = {
            "model": "gpt-3.5-turbo"
            # Faltando o campo "messages"
        }
        
        response = client.post("/v1/chat/completions", json=request_data)
        
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_chat_completions_endpoint_with_service_error(self):
        """Testa o endpoint de chat completions quando ocorre um erro no serviço"""
        with patch('app.services.langgraph_service.LangGraphService.process_chat_completion') as mock_service:
            mock_service.side_effect = Exception("Erro no serviço")
            
            request_data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": "Olá, como você está?"}
                ]
            }
            
            response = client.post("/v1/chat/completions", json=request_data)
            
            assert response.status_code == 500
            response_json = response.json()
            assert "detail" in response_json
            assert "Erro ao processar a requisição" in response_json["detail"]
# Testes para endpoints de agentes
class TestAgentsAPI:
    def test_agent_crud_flow(self):
        # Cria agente
        request = {"name": "test_agent", "description": "desc", "prompt": "p", "image": "img"}
        response = client.post("/v1/agents", json=request)
        assert response.status_code == 200
        data = response.json()
        assert "uuid" in data and data["name"] == "test_agent"
        agent_uuid = data["uuid"]
        # Obtém agente criado
        response = client.get(f"/v1/agents/{agent_uuid}")
        assert response.status_code == 200
        data_get = response.json()
        assert data_get["uuid"] == agent_uuid and data_get["name"] == "test_agent"
        # Lista agentes
        response = client.get("/v1/agents")
        assert response.status_code == 200
        agents_list = response.json()
        assert any(a["uuid"] == agent_uuid for a in agents_list)
        # Atualiza agente
        update_req = {"name": "updated", "description": "new_desc", "prompt": "new_p", "image": "new_img"}
        response = client.put(f"/v1/agents/{agent_uuid}", json=update_req)
        assert response.status_code == 200
        data_upd = response.json()
        assert data_upd["name"] == "updated" and data_upd["description"] == "new_desc"
        # Deleta agente
        response = client.delete(f"/v1/agents/{agent_uuid}")
        assert response.status_code == 204
        # Verifica exclusão
        response = client.get(f"/v1/agents/{agent_uuid}")
        assert response.status_code == 404