# hybrid-cache

Async hybrid Python cache with in-memory L1 caching, optional Redis L2 caching, pluggable invalidation, stampede protection, fail-safe stale values, and typed decorators.

## Documentation

The end-user documentation is in [`docs/`](docs/index.md) and is built with Zensical.

## Install

```bash
uv add hybrid-cache
```

Install optional providers only when your application uses them:

```bash
uv add "hybrid-cache[redis]"
uv add "hybrid-cache[rabbitmq]"
uv add "hybrid-cache[kafka]"
uv add "hybrid-cache[postgres]"
uv add "hybrid-cache[all]"
```

## Quick Start

```python
from hybrid_cache import CacheOptions, HybridCache, cached

cache = HybridCache(
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

For Redis-backed shared values and cross-instance invalidation, see the docs: [`docs/tutorials/get-started.md`](docs/tutorials/get-started.md).
