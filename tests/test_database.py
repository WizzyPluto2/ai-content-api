"""Tests for the database layer."""

import pytest

from database.connection import init_db
from database.repositories import (
    check_rate_limit,
    create_api_key,
    delete_api_key,
    get_content_by_id,
    get_recent_content,
    get_usage_stats,
    list_api_keys,
    log_usage,
    save_generated_content,
    validate_api_key,
)


@pytest.fixture(autouse=True)
async def setup_db():
    """Initialize database before each test."""
    await init_db()


class TestApiKeys:
    """Test API key CRUD operations."""

    @pytest.mark.asyncio
    async def test_create_api_key(self):
        result = await create_api_key("test-app")
        assert result["key"].startswith("ak_")
        assert result["name"] == "test-app"
        assert result["rate_limit"] == 60
        assert result["daily_limit"] == 1000

    @pytest.mark.asyncio
    async def test_create_key_custom_limits(self):
        result = await create_api_key("premium", rate_limit=120, daily_limit=5000)
        assert result["rate_limit"] == 120
        assert result["daily_limit"] == 5000

    @pytest.mark.asyncio
    async def test_validate_valid_key(self):
        created = await create_api_key("test")
        validated = await validate_api_key(created["key"])
        assert validated is not None
        assert validated["name"] == "test"

    @pytest.mark.asyncio
    async def test_validate_invalid_key(self):
        result = await validate_api_key("ak_invalid_key_12345")
        assert result is None

    @pytest.mark.asyncio
    async def test_list_api_keys(self):
        await create_api_key("key1")
        await create_api_key("key2")
        keys = await list_api_keys()
        assert len(keys) >= 2
        # Keys should be masked
        for k in keys:
            assert "..." in k["key_preview"]

    @pytest.mark.asyncio
    async def test_delete_api_key(self):
        created = await create_api_key("to-delete")
        assert await delete_api_key(created["key"]) is True
        validated = await validate_api_key(created["key"])
        assert validated is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_key(self):
        result = await delete_api_key("ak_nonexistent")
        assert result is False


class TestUsageLogging:
    """Test usage logging and stats."""

    @pytest.mark.asyncio
    async def test_log_usage(self):
        key = await create_api_key("test")
        await log_usage(key["key"], "blog-post", "openai", 100)
        stats = await get_usage_stats(key["key"])
        assert stats["today"]["requests"] == 1
        assert stats["today"]["tokens"] == 100

    @pytest.mark.asyncio
    async def test_usage_stats_breakdown(self):
        key = await create_api_key("test")
        await log_usage(key["key"], "blog-post", "openai", 100)
        await log_usage(key["key"], "social-media", "gemini", 50)
        stats = await get_usage_stats(key["key"])
        assert stats["total"]["requests"] == 2
        assert stats["total"]["tokens"] == 150
        assert "openai" in stats["by_provider"]
        assert "gemini" in stats["by_provider"]

    @pytest.mark.asyncio
    async def test_empty_usage_stats(self):
        key = await create_api_key("test")
        stats = await get_usage_stats(key["key"])
        assert stats["today"]["requests"] == 0
        assert stats["total"]["tokens"] == 0


class TestRateLimiting:
    """Test rate limit checking."""

    @pytest.mark.asyncio
    async def test_within_limits(self):
        key = await create_api_key("test")
        result = await check_rate_limit(key["key"], rate_limit=60, daily_limit=1000)
        assert result is True

    @pytest.mark.asyncio
    async def test_exceeds_daily_limit(self):
        key = await create_api_key("test")
        # Log enough to exceed daily limit
        for _ in range(5):
            await log_usage(key["key"], "test", "mock", 10)
        result = await check_rate_limit(key["key"], rate_limit=60, daily_limit=3)
        assert result is False


class TestGeneratedContent:
    """Test generated content storage."""

    @pytest.mark.asyncio
    async def test_save_and_retrieve(self):
        key = await create_api_key("test")
        content_id = await save_generated_content(
            api_key=key["key"],
            template_id="blog-post",
            provider="openai",
            input_data={"topic": "test"},
            output_content="Generated blog post content",
            tokens_used=100,
        )
        assert content_id > 0

        content = await get_content_by_id(content_id)
        assert content is not None
        assert content["output_content"] == "Generated blog post content"
        assert content["tokens_used"] == 100

    @pytest.mark.asyncio
    async def test_recent_content(self):
        key = await create_api_key("test")
        await save_generated_content(key["key"], "blog-post", "openai", {}, "content 1", 50)
        await save_generated_content(key["key"], "email", "gemini", {}, "content 2", 30)
        recent = await get_recent_content(key["key"], limit=10)
        assert len(recent) == 2

    @pytest.mark.asyncio
    async def test_content_not_found(self):
        content = await get_content_by_id(99999)
        assert content is None
