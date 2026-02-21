"""Tests for API key authentication middleware."""

from unittest.mock import patch

import pytest
from fastapi import HTTPException

from database.connection import init_db
from database.repositories import create_api_key
from middleware import get_api_key


@pytest.fixture(autouse=True)
async def setup_db():
    await init_db()


class TestApiKeyAuth:
    """Test API key authentication."""

    @pytest.mark.asyncio
    async def test_missing_key_raises_401(self):
        with pytest.raises(HTTPException) as exc:
            await get_api_key(api_key=None)
        assert exc.value.status_code == 401

    @pytest.mark.asyncio
    async def test_invalid_key_raises_403(self):
        with pytest.raises(HTTPException) as exc:
            await get_api_key(api_key="ak_invalid_key")
        assert exc.value.status_code == 403

    @pytest.mark.asyncio
    async def test_valid_key_returns_data(self):
        created = await create_api_key("test")
        result = await get_api_key(api_key=created["key"])
        assert result["name"] == "test"
        assert result["key"] == created["key"]

    @pytest.mark.asyncio
    async def test_master_key(self):
        with patch("middleware.settings") as mock_settings:
            mock_settings.master_api_key = "master-secret-key"
            result = await get_api_key(api_key="master-secret-key")
            assert result["name"] == "master"
            assert result["rate_limit"] == 9999

    @pytest.mark.asyncio
    async def test_rate_limited_key_raises_429(self):
        created = await create_api_key("test", rate_limit=1, daily_limit=1)
        # First call should work
        result = await get_api_key(api_key=created["key"])
        assert result is not None

        # Simulate usage to trigger rate limit
        from database.repositories import log_usage

        await log_usage(created["key"], "test", "mock", 10)

        with pytest.raises(HTTPException) as exc:
            await get_api_key(api_key=created["key"])
        assert exc.value.status_code == 429
