# hybrid-cache

Async hybrid Python cache with in-memory L1 caching, optional distributed L2 caching, pluggable invalidation, stampede protection, fail-safe stale values, and typed decorators.

## Development

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
uv build --no-sources
```

## Optional Providers

```bash
uv add "hybrid-cache[redis]"
uv add "hybrid-cache[rabbitmq]"
uv add "hybrid-cache[kafka]"
uv add "hybrid-cache[postgres]"
uv add "hybrid-cache[all]"
```

## Usage

```python
from redis.asyncio import Redis

from hybrid_cache import (
    CacheOptions,
    HybridCache,
    RedisDistributedCache,
    RedisStreamsInvalidationBus,
    cached,
)

redis = Redis.from_url("redis://localhost:6379/0", decode_responses=False)
cache = HybridCache(
    distributed_cache=RedisDistributedCache(redis),
    invalidation_bus=RedisStreamsInvalidationBus(redis),
    options=CacheOptions(
        ttl_seconds=60,
        fail_safe_seconds=300,
        hard_timeout_seconds=5,
        jitter_seconds=5,
    ),
)

await cache.start()


@cached(cache)
async def get_user(user_id: str) -> dict[str, str]:
    return {"id": user_id, "name": "Peter"}


user = await get_user("123")
await get_user.remove_cached("123")
await cache.stop()
```

By default, `@cached(cache)` builds keys from the function module, qualified name, and bound arguments. Pass a string or callable key when you want to share a key across functions or customize the key shape:

```python
@cached(cache, lambda user_id: f"user:{user_id}")
async def get_user(user_id: str) -> dict[str, str]:
    ...
```

## Architecture

```text
HybridCache
|- optional DistributedCache
`- optional InvalidationBus
```

- `DistributedCache` stores shared L2 values. Redis is one implementation.
- `InvalidationBus` publishes cache invalidations and applies received messages to the local L1 cache.
- `RedisStreamsInvalidationBus` implements Redis Streams invalidation directly.
- The two axes are independent: an invalidation bus can be used without a distributed cache, and any invalidation bus can be paired with any distributed cache.

| Provider | Distributed cache | Invalidation bus |
| --- | --- | --- |
| Redis | `RedisDistributedCache` | `RedisStreamsInvalidationBus` |
| RabbitMQ | - | `RabbitMQInvalidationBus` |
| Kafka | - | `KafkaInvalidationBus` |
| PostgreSQL | - | `PostgresNotifyInvalidationBus` |

Kafka invalidation uses a unique consumer group per node by default so every cache instance receives every invalidation. Sharing a Kafka consumer group between cache instances load-balances messages and is not appropriate for cache invalidation.

Reads follow this order:

```text
memory L1 -> distributed L2 -> factory
```

The default Redis serializer uses `pickle`. Only use it when Redis data is trusted. Supply a custom `Serializer` for JSON, msgpack, or another format.
