"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from database.connection import init_db


@pytest.fixture(autouse=True)
async def setup_db():
    await init_db()


@pytest.fixture
def client():
    from app import app

    return TestClient(app)


class TestHealthEndpoint:
    """Test GET /api/health."""

    def test_health_returns_200(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "providers" in data


class TestTemplateEndpoints:
    """Test template listing endpoints."""

    def test_list_templates(self, client):
        response = client.get("/api/templates")
        assert response.status_code == 200
        data = response.json()
        assert "templates" in data
        assert len(data["templates"]) >= 8

    def test_get_template_by_id(self, client):
        response = client.get("/api/templates/blog-post")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "blog-post"
        assert "fields" in data

    def test_get_nonexistent_template(self, client):
        response = client.get("/api/templates/nonexistent")
        assert response.status_code == 404


class TestProviderEndpoints:
    """Test provider listing endpoint."""

    def test_list_providers(self, client):
        response = client.get("/api/providers")
        assert response.status_code == 200
        data = response.json()
        assert "providers" in data
        assert len(data["providers"]) > 0


class TestKeyEndpoints:
    """Test API key management endpoints."""

    def test_create_key(self, client):
        response = client.post("/api/keys?name=test-key")
        assert response.status_code == 200
        data = response.json()
        assert data["key"].startswith("ak_")
        assert data["name"] == "test-key"

    def test_list_keys(self, client):
        client.post("/api/keys?name=key1")
        client.post("/api/keys?name=key2")
        response = client.get("/api/keys")
        assert response.status_code == 200
        assert len(response.json()["keys"]) >= 2

    @pytest.mark.asyncio
    async def test_get_key_usage(self, client):
        res = client.post("/api/keys?name=test")
        key = res.json()["key"]
        response = client.get(f"/api/keys/{key}/usage")
        assert response.status_code == 200
        data = response.json()
        assert "today" in data
        assert "total" in data

    def test_get_nonexistent_key_usage(self, client):
        response = client.get("/api/keys/ak_fake_key/usage")
        assert response.status_code == 404


class TestGenerateEndpoint:
    """Test POST /api/generate."""

    def test_generate_requires_api_key(self, client):
        response = client.post(
            "/api/generate",
            json={"template_id": "blog-post", "variables": {"topic": "test"}},
        )
        assert response.status_code == 401

    def test_generate_invalid_key(self, client):
        response = client.post(
            "/api/generate",
            json={"template_id": "blog-post", "variables": {"topic": "test"}},
            headers={"X-API-Key": "ak_invalid"},
        )
        assert response.status_code == 403

    def test_generate_invalid_template(self, client):
        res = client.post("/api/keys?name=test")
        key = res.json()["key"]
        response = client.post(
            "/api/generate",
            json={"template_id": "nonexistent", "variables": {}},
            headers={"X-API-Key": key},
        )
        assert response.status_code == 404

    def test_generate_missing_required_field(self, client):
        res = client.post("/api/keys?name=test")
        key = res.json()["key"]
        response = client.post(
            "/api/generate",
            json={"template_id": "blog-post", "variables": {}},
            headers={"X-API-Key": key},
        )
        assert response.status_code == 422


class TestDashboard:
    """Test dashboard serving."""

    def test_dashboard_serves_html(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
