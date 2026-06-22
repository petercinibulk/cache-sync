"""PostgreSQL provider exports."""

from cache_sync.providers.postgres.invalidation_bus import PostgresNotifyInvalidationBus

__all__ = [
    "PostgresNotifyInvalidationBus",
]
