import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestHealthEndpoints:
    """Testes para os endpoints de health check"""
    
    def test_health_status_endpoint(self):
        """Testa o endpoint de health check básico"""
        response = client.get("/health/status")
        assert response.status_code == 200
        response_json = response.json()
        assert "status" in response_json
        assert response_json["status"] == "healthy"
        assert "timestamp" in response_json
        assert "service" in response_json
        assert response_json["service"] == "FastAPI com LangGraph"
    
    def test_detailed_health_check_endpoint(self):
        """Testa o endpoint de health check detalhado"""
        response = client.get("/health/detailed")
        assert response.status_code == 200
        response_json = response.json()
        assert "status" in response_json
        assert response_json["status"] == "healthy"
        assert "timestamp" in response_json
        assert "service" in response_json
        assert response_json["service"] == "FastAPI com LangGraph"
        assert "system" in response_json
        assert "service_status" in response_json
    
    def test_readiness_check_endpoint(self):
        """Testa o endpoint de readiness check"""
        response = client.get("/health/ready")
        assert response.status_code == 200
        response_json = response.json()
        assert "status" in response_json
        assert response_json["status"] in ["ready", "not_ready"]
        assert "timestamp" in response_json
        assert "dependencies" in response_json