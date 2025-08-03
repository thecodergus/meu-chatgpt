import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.services.langgraph_service import LangGraphService

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_llm(monkeypatch):
    # Mocka a chamada ao provedor LLM para retornar resposta fixa
    monkeypatch.setattr(
        LangGraphService,
        "process_chat_completion",
        lambda self, messages, model, provider, temperature, top_p, max_tokens, functions, function_call: "resposta teste"
    )
    yield

def test_create_conversation():
    response = client.post("/v1/conversations", json={})
    assert response.status_code == 200
    data = response.json()
    assert "thread_uuid" in data
    assert isinstance(data["thread_uuid"], str)

def test_list_conversations_initially_empty():
    response = client.get("/v1/conversations")
    assert response.status_code == 200
    assert response.json() == []

def test_send_and_retrieve_message():
    # Cria nova conversa
    resp = client.post("/v1/conversations", json={})
    tid = resp.json()["thread_uuid"]
    # Envia mensagem de usuário
    payload = {
        "messages": [{"role": "user", "content": "Olá"}],
        "model": "test",
        "provider": "mock"
    }
    resp2 = client.post(f"/v1/conversations/{tid}/messages", json=payload)
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["choices"][0]["message"]["content"] == "resposta teste"
    # Recupera conversa completa
    resp3 = client.get(f"/v1/conversations/{tid}")
    conv = resp3.json()
    assert conv["messages"][0]["role"] == "user"
    assert conv["messages"][1]["role"] == "assistant"

def test_get_conversation_not_found():
    fake_id = str(uuid.uuid4())
    response = client.get(f"/v1/conversations/{fake_id}")
    assert response.status_code == 404