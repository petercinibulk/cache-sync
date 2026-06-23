# cache-sync

Async hybrid Python cache with in-memory L1 caching, optional Redis or Memcached L2 caching, pluggable invalidation, stampede protection, fail-safe stale values, and typed decorators.

## Features

- Async-first API for Python 3.12 and newer.
- Fast in-process L1 cache with optional Redis-backed or Memcached-backed L2 storage.
- Pluggable invalidation buses for Redis Streams, RabbitMQ, Kafka, and PostgreSQL.
- Request stampede protection with per-key refresh coordination.
- Fail-safe stale reads for short backend outages.
- Typed decorators that preserve the wrapped function signature.
- Serializer choices for JSON, pickle, and Pydantic models.

## Documentation

The end-user documentation is published at <https://petercinibulk.github.io/cache-sync/> and is built from [`docs/`](docs/index.md) with Zensical.

## Install

```bash
uv add cache-sync
```

Install optional providers only when your application uses them:

```bash
uv add "cache-sync[redis]"
uv add "cache-sync[memcache]"
uv add "cache-sync[rabbitmq]"
uv add "cache-sync[kafka]"
uv add "cache-sync[postgres]"
uv add "cache-sync[all]"
```

| Extra | Installs | Use when |
| --- | --- | --- |
| `redis` | `redis` | You need Redis L2 storage or Redis Streams invalidation. |
| `memcache` | `aiomcache` | You need Memcached L2 storage. |
| `rabbitmq` | `aio-pika` | You use RabbitMQ as the invalidation bus. |
| `kafka` | `aiokafka` | You use Kafka as the invalidation bus. |
| `postgres` | `asyncpg` | You use PostgreSQL `LISTEN`/`NOTIFY` for invalidation. |
| `pydantic` | `pydantic` | You want Pydantic model serialization helpers. |
| `all` | all provider dependencies | You want every optional provider available. |

## Quick Start

```python
from cache_sync import CacheOptions, CacheSync

cache = CacheSync(
    options=CacheOptions(
        ttl_seconds=60,
        fail_safe_seconds=300,
        hard_timeout_seconds=5,
        jitter_seconds=5,
    ),
)

await cache.start()


@cache.cached(lambda user_id: f"user:{user_id}")
async def get_user(user_id: str) -> dict[str, str]:
    return {"id": user_id, "name": "Peter"}


user = await get_user("123")
await get_user.remove_cached("123")
await cache.stop()
```

## Redis L2 Example

```python
from redis.asyncio import Redis

from cache_sync import CacheOptions, CacheSync, RedisDistributedCache

redis = Redis.from_url("redis://localhost:6379/0")

cache = CacheSync(
    distributed_cache=RedisDistributedCache(redis),
    options=CacheOptions(ttl_seconds=60, fail_safe_seconds=300),
)

await cache.start()


@cache.cached(lambda product_id: f"product:{product_id}")
async def get_product(product_id: str) -> dict[str, str]:
    return {"id": product_id}
```

For a complete walkthrough with shared values and cross-instance invalidation, see the [get started tutorial](https://petercinibulk.github.io/cache-sync/tutorials/get-started/).

## Memcached L2 Example

```python
import aiomcache

from cache_sync import CacheOptions, CacheSync, MemcachedDistributedCache

memcache = aiomcache.Client("127.0.0.1", 11211)

cache = CacheSync(
    distributed_cache=MemcachedDistributedCache(memcache),
    options=CacheOptions(ttl_seconds=60, fail_safe_seconds=300),
)
```

## Project

- License: MIT
- Source: <https://github.com/petercinibulk/cache-sync>
- Issues: <https://github.com/petercinibulk/cache-sync/issues>
