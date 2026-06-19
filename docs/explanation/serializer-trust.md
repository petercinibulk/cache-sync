# Serializer Trust

The Redis distributed cache stores bytes. A serializer decides how application values become bytes and how bytes become application values again.

`RedisDistributedCache` uses `PickleSerializer` by default because it can handle many Python objects. Pickle is only appropriate when Redis data is trusted by your application. Do not use pickle for data that untrusted users or systems can write.

Use `JsonSerializer` for JSON-compatible values when you want a simple, inspectable format. Use `PydanticSerializer` when cached values are Pydantic models and you want model-aware loading.

Serializer choice affects the distributed L2 cache. It does not affect local L1 memory values.
