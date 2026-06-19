"""RabbitMQ provider exports."""

from hybrid_cache.providers.rabbitmq.invalidation_bus import RabbitMQInvalidationBus

__all__ = [
    "RabbitMQInvalidationBus",
]
