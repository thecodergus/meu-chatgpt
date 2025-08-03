import requests
import pytest

BASE_URL = "http://localhost:8000/v1"

def test_create_conversation_default_agent():
    response = requests.post(f"{BASE_URL}/conversations", json={})
    assert response.status_code == 200
    data = response.json()
    assert "thread_uuid" in data
    assert isinstance(data["thread_uuid"], str)

def test_get_conversation_default_tools():
    # Lista conversas e verifica a última criada
    response = requests.get(f"{BASE_URL}/conversations")
    assert response.status_code == 200
    convs = response.json()
    assert isinstance(convs, list) and convs
    conv = convs[-1]
    # Agente padrão deve ser None
    assert conv["agent_uuid"] is None
    # tools_enabled deve ser lista de strings
    assert isinstance(conv["tools_enabled"], list)
    assert all(isinstance(t, str) for t in conv["tools_enabled"])