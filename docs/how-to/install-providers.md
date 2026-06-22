# Install Optional Providers

`Cache-Sync` has no required runtime dependencies. Install only the providers your application uses.

## Redis distributed cache and Redis Streams invalidation

```bash
uv add "cache-sync[redis]"
```

Use this when Redis should store shared cached values, carry invalidation messages, or both.

## RabbitMQ invalidation

```bash
uv add "cache-sync[rabbitmq]"
```

Use this when your application already has RabbitMQ and only needs invalidation messages between instances.

## Kafka invalidation

```bash
uv add "cache-sync[kafka]"
```

Use this when Kafka is already part of your platform and every cache instance must receive each invalidation.

## PostgreSQL notification invalidation

```bash
uv add "cache-sync[postgres]"
```

Use this for PostgreSQL `LISTEN`/`NOTIFY` invalidation when you do not want to run a separate message broker.

## All optional providers

```bash
uv add "cache-sync[all]"
```

Use this for experiments or shared application templates. Production apps usually install only the extras they need.
