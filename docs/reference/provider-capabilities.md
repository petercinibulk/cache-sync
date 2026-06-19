# Provider Capabilities

| Provider | Distributed cache | Invalidation bus | Notes |
| --- | --- | --- | --- |
| Redis | `RedisDistributedCache` | `RedisStreamsInvalidationBus` | Can provide both shared values and invalidation |
| RabbitMQ | No | `RabbitMQInvalidationBus` | Uses a fanout exchange |
| Kafka | No | `KafkaInvalidationBus` | Uses a topic and a unique consumer group per node by default |
| PostgreSQL | No | `PostgresNotifyInvalidationBus` | Uses `LISTEN`/`NOTIFY` |

Distributed cache and invalidation are independent. You can use Redis for shared cached values without an invalidation bus, an invalidation bus without shared L2 storage, or both together.

## Default names

| Provider | Default name |
| --- | --- |
| Redis distributed key prefix | `hybrid-cache:` |
| Redis invalidation stream | `hybrid-cache:invalidations` |
| RabbitMQ exchange | `hybrid-cache-invalidations` |
| Kafka topic | `hybrid-cache-invalidations` |
| PostgreSQL channel | `hybrid_cache_invalidations` |
