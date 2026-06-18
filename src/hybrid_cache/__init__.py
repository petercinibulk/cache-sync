from typing import TYPE_CHECKING, Any

from hybrid_cache.core import CacheOptions, HybridCache
from hybrid_cache.decorators import CachedFunction, cached
from hybrid_cache.distributed_cache import DistributedCache
from hybrid_cache.invalidation import (
    InvalidationBus,
    InvalidationHandler,
    InvalidationMessage,
    InvalidationTransport,
    TransportInvalidationBus,
)
from hybrid_cache.serializers import (
    JsonSerializer,
    PickleSerializer,
    PydanticSerializer,
    Serializer,
)

if TYPE_CHECKING:
    from hybrid_cache.providers.kafka import KafkaInvalidationBus
    from hybrid_cache.providers.postgres import PostgresNotifyInvalidationBus
    from hybrid_cache.providers.rabbitmq import RabbitMQInvalidationBus
    from hybrid_cache.providers.redis import (
        RedisDistributedCache,
        RedisStreamsInvalidationBus,
    )

__all__ = [
    "CacheOptions",
    "CachedFunction",
    "DistributedCache",
    "HybridCache",
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
    "cached",
]


def __getattr__(name: str) -> Any:
    if name == "RedisDistributedCache":
        from hybrid_cache.providers.redis import RedisDistributedCache

        return RedisDistributedCache

    if name == "RedisStreamsInvalidationBus":
        from hybrid_cache.providers.redis import RedisStreamsInvalidationBus

        return RedisStreamsInvalidationBus

    if name == "RabbitMQInvalidationBus":
        from hybrid_cache.providers.rabbitmq import RabbitMQInvalidationBus

        return RabbitMQInvalidationBus

    if name == "KafkaInvalidationBus":
        from hybrid_cache.providers.kafka import KafkaInvalidationBus

        return KafkaInvalidationBus

    if name == "PostgresNotifyInvalidationBus":
        from hybrid_cache.providers.postgres import PostgresNotifyInvalidationBus

        return PostgresNotifyInvalidationBus

    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)
