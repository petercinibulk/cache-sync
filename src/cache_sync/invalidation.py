from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Literal, Protocol

type InvalidationAction = Literal["remove", "clear"]
type RemoveLocal = Callable[[str], None]
type ClearLocal = Callable[[], None]


@dataclass(frozen=True, slots=True)
class InvalidationMessage:
    """Message sent between cache nodes to remove keys or clear local memory."""

    action: InvalidationAction
    key: str | None = None

    @classmethod
    def remove(cls, key: str) -> InvalidationMessage:
        """Create a message that removes one key from peer local caches."""

        return cls(action="remove", key=key)

    @classmethod
    def clear(cls) -> InvalidationMessage:
        """Create a message that clears peer local caches."""

        return cls(action="clear")


type InvalidationHandler = Callable[[InvalidationMessage], Awaitable[None]]


class InvalidationTransport(Protocol):
    """Low-level transport used by `TransportInvalidationBus`."""

    async def start(self, handler: InvalidationHandler) -> None: ...

    async def stop(self) -> None: ...

    async def publish(self, message: InvalidationMessage) -> None: ...


class InvalidationBus(Protocol):
    """Protocol for publishing and receiving cache invalidation events."""

    async def start(
        self,
        *,
        remove_local: RemoveLocal,
        clear_local: ClearLocal,
    ) -> None: ...

    async def stop(self) -> None: ...

    async def invalidate(self, key: str) -> None: ...

    async def clear(self) -> None: ...


class TransportInvalidationBus:
    """Adapt an `InvalidationTransport` into the `InvalidationBus` protocol."""

    def __init__(self, transport: InvalidationTransport) -> None:
        """Create an invalidation bus backed by a generic transport."""

        self._transport = transport
        self._remove_local: RemoveLocal | None = None
        self._clear_local: ClearLocal | None = None

    async def start(
        self,
        *,
        remove_local: RemoveLocal,
        clear_local: ClearLocal,
    ) -> None:
        """Start listening for remote invalidation messages."""

        self._remove_local = remove_local
        self._clear_local = clear_local
        await self._transport.start(self._handle_message)

    async def stop(self) -> None:
        """Stop listening and release local callbacks."""

        await self._transport.stop()
        self._remove_local = None
        self._clear_local = None

    async def invalidate(self, key: str) -> None:
        """Publish a message instructing peers to remove one key."""

        await self._transport.publish(InvalidationMessage.remove(key))

    async def clear(self) -> None:
        """Publish a message instructing peers to clear local memory."""

        await self._transport.publish(InvalidationMessage.clear())

    async def _handle_message(self, message: InvalidationMessage) -> None:
        remove_local = self._remove_local
        clear_local = self._clear_local

        if message.action == "remove" and message.key is not None:
            if remove_local is not None:
                remove_local(message.key)
            return

        if message.action == "clear" and clear_local is not None:
            clear_local()
