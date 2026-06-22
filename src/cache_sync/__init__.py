"""Public API for cache-sync."""

from typing import TYPE_CHECKING, Any

from cache_sync.core import CacheOptions, CacheSync
from cache_sync.decorators import CachedFunction
from cache_sync.distributed_cache import DistributedCache
from cache_sync.invalidation import (
    InvalidationBus,
    InvalidationHandler,
    InvalidationMessage,
    InvalidationTransport,
    TransportInvalidationBus,
)
from cache_sync.serializers import (
    JsonSerializer,
    PickleSerializer,
    PydanticSerializer,
    Serializer,
)

if TYPE_CHECKING:
    from cache_sync.providers.kafka import KafkaInvalidationBus
    from cache_sync.providers.postgres import PostgresNotifyInvalidationBus
    from cache_sync.providers.rabbitmq import RabbitMQInvalidationBus
    from cache_sync.providers.redis import (
        RedisDistributedCache,
        RedisStreamsInvalidationBus,
    )

__all__ = [
    "CacheOptions",
    "CacheSync",
    "CachedFunction",
    "DistributedCache",
    "InvalidationBus",
    "InvalidationHandler",
    "InvalidationMessage",
    "InvalidationTransport",
    "JsonSerializer",
    "KafkaInvalidationBus",
    "PickleSerializer",
    "PostgresNotifyInvalidationBus",
    "PydanticSerializer",
    "RabbitMQInvalidationBus",
    "RedisDistributedCache",
    "RedisStreamsInvalidationBus",
    "Serializer",
    "TransportInvalidationBus",
]


def __getattr__(name: str) -> Any:
    if name == "RedisDistributedCache":
        from cache_sync.providers.redis import RedisDistributedCache

        return RedisDistributedCache

    if name == "RedisStreamsInvalidationBus":
        from cache_sync.providers.redis import RedisStreamsInvalidationBus

        return RedisStreamsInvalidationBus

    if name == "RabbitMQInvalidationBus":
        from cache_sync.providers.rabbitmq import RabbitMQInvalidationBus

        return RabbitMQInvalidationBus

    if name == "KafkaInvalidationBus":
        from cache_sync.providers.kafka import KafkaInvalidationBus

        return KafkaInvalidationBus

    if name == "PostgresNotifyInvalidationBus":
        from cache_sync.providers.postgres import PostgresNotifyInvalidationBus

        return PostgresNotifyInvalidationBus

    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)
