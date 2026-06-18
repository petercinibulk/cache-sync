# hybrid-cache

Async hybrid Python cache with:

- in-memory L1 cache
- optional Redis L2 cache
- Redis Streams distributed invalidation
- per-key stampede protection
- fail-safe stale fallback
- type-safe decorator API
- helper methods such as `remove_cached()` on decorated functions

## Install

```bash
uv add hybrid-cache
```

For local development:

```bash
git clone https://github.com/petercinibulk/hybrid-cache.git
cd hybrid-cache
uv sync
uv run ruff check .
uv run ruff format .
uv run ty check
uv run pytest
```

## Usage

```python
from redis.asyncio import Redis

from hybrid_cache import CacheOptions, HybridCache, cached

redis = Redis.from_url("redis://localhost:6379/0", decode_responses=False)
cache = HybridCache(
    redis=redis,
    options=CacheOptions(
        ttl_seconds=60,
        fail_safe_seconds=300,
        hard_timeout_seconds=5,
        jitter_seconds=5,
    ),
)

await cache.start()


@cached(cache, lambda user_id: f"user:{user_id}")
async def get_user(user_id: str) -> dict[str, str]:
    return {"id": user_id, "name": "Peter"}


user = await get_user("123")
await get_user.remove_cached("123")

await cache.stop()
```

## How it works

Reads follow this order:

```text
memory L1 -> Redis L2 -> factory
```

Writes and removals publish Redis Streams invalidation events so other nodes drop stale local memory entries. Each node gets its own consumer group, which makes stream events broadcast-style instead of load-balanced across nodes.

## Notes

The default Redis serializer uses `pickle`, which is convenient for trusted internal services. Do not use pickle for untrusted Redis data. A custom `Serializer` can be supplied for JSON, msgpack, or application-specific serialization.
