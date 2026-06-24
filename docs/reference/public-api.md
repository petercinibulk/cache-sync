# Public API

Import these names from `cache_sync` for normal application use.

```python
from cache_sync import CacheOptions, CacheSync, ScopedCache
```

## Cache

| Name | Purpose |
| --- | --- |
| `CacheSync` | Coordinates local memory, optional distributed storage, invalidation, and lifecycle. |
| `CacheOptions` | Configures TTL, stale reads, timeouts, jitter, and per-scope LRU limits. |
| `CacheSync.cached` | Decorates an async function and adds cache lookup, set, and removal behavior. |
| `CachedFunction` | Wrapper for decorated functions with `remove_cached` and `cache_key` helpers. |
| `DistributedCache` | Protocol implemented by shared cache providers such as Redis. |
| `ScopedCache` | Manual scoped cache view with scoped get, set, remove, clear, and LRU policy. |

## Invalidation

| Name | Purpose |
| --- | --- |
| `InvalidationBus` | Protocol for local cache invalidation across application instances. |
| `InvalidationMessage` | Message model for removing one key or clearing local cache entries. |
| `InvalidationHandler` | Callback type used by invalidation transports. |
| `InvalidationTransport` | Protocol for transports that publish and subscribe to invalidation messages. |
| `TransportInvalidationBus` | Adapter that builds an `InvalidationBus` from an `InvalidationTransport`. |

## Providers

Provider classes are lazily imported so optional dependencies are only required when you use that provider.

| Name | Extra | Purpose |
| --- | --- | --- |
| `RedisDistributedCache` | `redis` | Stores shared cached values in Redis. |
| `RedisStreamsInvalidationBus` | `redis` | Publishes invalidations through Redis Streams. |
| `RabbitMQInvalidationBus` | `rabbitmq` | Publishes invalidations through a RabbitMQ fanout exchange. |
| `KafkaInvalidationBus` | `kafka` | Publishes invalidations through a Kafka topic. |
| `PostgresNotifyInvalidationBus` | `postgres` | Publishes invalidations through PostgreSQL `LISTEN`/`NOTIFY`. |

## Serializers

| Name | Purpose |
| --- | --- |
| `Serializer` | Protocol for converting values to and from bytes. |
| `JsonSerializer` | Serializes JSON-compatible values. |
| `PickleSerializer` | Serializes trusted Python objects with pickle. |
| `PydanticSerializer` | Serializes Pydantic models. |

## Type information

`cache-sync` ships a `py.typed` marker. Type checkers can use the inline annotations from the installed package.
