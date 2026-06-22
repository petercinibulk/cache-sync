from __future__ import annotations

from cache_sync.invalidation import (
    InvalidationHandler,
    InvalidationMessage,
    TransportInvalidationBus,
)


class FakeTransport:
    def __init__(self) -> None:
        self.handler: InvalidationHandler | None = None
        self.published: list[InvalidationMessage] = []

    async def start(self, handler: InvalidationHandler) -> None:
        self.handler = handler

    async def stop(self) -> None:
        self.handler = None

    async def publish(self, message: InvalidationMessage) -> None:
        self.published.append(message)

    async def emit(self, message: InvalidationMessage) -> None:
        if self.handler is not None:
            await self.handler(message)


async def test_transport_invalidation_bus_publishes_and_applies_messages() -> None:
    transport = FakeTransport()
    bus = TransportInvalidationBus(transport)
    removed: list[str] = []
    clear_count = 0

    def clear_local() -> None:
        nonlocal clear_count
        clear_count += 1

    await bus.start(remove_local=removed.append, clear_local=clear_local)
    await bus.invalidate("user:1")
    await bus.clear()

    assert transport.published == [
        InvalidationMessage.remove("user:1"),
        InvalidationMessage.clear(),
    ]

    await transport.emit(InvalidationMessage.remove("user:2"))
    await transport.emit(InvalidationMessage.clear())

    assert removed == ["user:2"]
    assert clear_count == 1


async def test_transport_invalidation_bus_uses_transport_without_cache_storage() -> None:
    transport = FakeTransport()
    bus = TransportInvalidationBus(transport)
    removed: list[str] = []

    await bus.start(remove_local=removed.append, clear_local=lambda: None)
    await bus.invalidate("user:1")
    await transport.emit(InvalidationMessage.remove("user:2"))

    assert transport.published == [InvalidationMessage.remove("user:1")]
    assert removed == ["user:2"]
