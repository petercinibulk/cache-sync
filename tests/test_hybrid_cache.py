from __future__ import annotations

import asyncio

import pytest

from hybrid_cache import CacheOptions, HybridCache, cached


@pytest.mark.asyncio
async def test_get_or_set_returns_cached_value() -> None:
    cache = HybridCache(options=CacheOptions(ttl_seconds=60))
    calls = 0

    async def factory() -> str:
        nonlocal calls
        calls += 1
        return "value"

    first = await cache.get_or_set("key", factory)
    second = await cache.get_or_set("key", factory)

    assert first == "value"
    assert second == "value"
    assert calls == 1


@pytest.mark.asyncio
async def test_get_or_set_prevents_stampede() -> None:
    cache = HybridCache(options=CacheOptions(ttl_seconds=60))
    calls = 0

    async def factory() -> str:
        nonlocal calls
        calls += 1
        await asyncio.sleep(0.01)
        return "value"

    values = await asyncio.gather(*(cache.get_or_set("key", factory) for _ in range(10)))

    assert values == ["value"] * 10
    assert calls == 1


@pytest.mark.asyncio
async def test_fail_safe_returns_stale_value() -> None:
    cache = HybridCache(options=CacheOptions(ttl_seconds=0.01, fail_safe_seconds=60))

    async def working_factory() -> str:
        return "stale"

    await cache.get_or_set("key", working_factory)
    await asyncio.sleep(0.02)

    async def failing_factory() -> str:
        raise RuntimeError("factory failed")

    value = await cache.get_or_set("key", failing_factory)

    assert value == "stale"


@pytest.mark.asyncio
async def test_remove_deletes_cached_value() -> None:
    cache = HybridCache(options=CacheOptions(ttl_seconds=60))
    calls = 0

    async def factory() -> str:
        nonlocal calls
        calls += 1
        return f"value-{calls}"

    assert await cache.get_or_set("key", factory) == "value-1"
    await cache.remove("key")
    assert await cache.get_or_set("key", factory) == "value-2"


@pytest.mark.asyncio
async def test_decorator_preserves_return_type_and_remove_cached() -> None:
    cache = HybridCache(options=CacheOptions(ttl_seconds=60))
    calls = 0

    @cached(cache, lambda user_id: f"user:{user_id}")
    async def get_user(user_id: str) -> dict[str, str]:
        nonlocal calls
        calls += 1
        return {"id": user_id}

    first = await get_user("123")
    second = await get_user("123")
    await get_user.remove_cached("123")
    third = await get_user("123")

    assert first == {"id": "123"}
    assert second == {"id": "123"}
    assert third == {"id": "123"}
    assert calls == 2
    assert get_user.cache_key("123") == "user:123"
