"""RabbitMQ provider exports."""

from cache_sync.providers.rabbitmq.invalidation_bus import RabbitMQInvalidationBus

__all__ = [
    "RabbitMQInvalidationBus",
]
