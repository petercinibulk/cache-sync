from __future__ import annotations

import json
import socket
import uuid
from typing import Any

from hybrid_cache.invalidation import (
    ClearLocal,
    InvalidationMessage,
    RemoveLocal,
)


class PostgresNotifyInvalidationBus:
    def __init__(
        self,
        connection: Any,
        *,
        channel: str = "hybrid_cache_invalidations",
        node_name: str | None = None,
    ) -> None:
        self._connection = connection
        self._channel = channel
        self._source_id = str(uuid.uuid4())
        self._node_name = node_name or f"{socket.gethostname()}-{self._source_id}"
        self._remove_local: RemoveLocal | None = None
        self._clear_local: ClearLocal | None = None
        self._started = False

    async def start(
        self,
        *,
        remove_local: RemoveLocal,
        clear_local: ClearLocal,
    ) -> None:
        if self._started:
            return

        self._remove_local = remove_local
        self._clear_local = clear_local
        await self._connection.add_listener(self._channel, self._handle_notification)
        self._started = True

    async def stop(self) -> None:
        if self._started:
            await self._connection.remove_listener(self._channel, self._handle_notification)

        self._started = False
        self._remove_local = None
        self._clear_local = None

    async def invalidate(self, key: str) -> None:
        await self._publish(InvalidationMessage.remove(key))

    async def clear(self) -> None:
        await self._publish(InvalidationMessage.clear())

    async def _publish(self, message: InvalidationMessage) -> None:
        await self._connection.execute(
            "select pg_notify($1, $2)",
            self._channel,
            self._encode_message(message),
        )

    def _handle_notification(
        self,
        connection: Any,
        pid: int,
        channel: str,
        payload: str,
    ) -> None:
        del connection, pid, channel
        message = self._decode_message(payload)

        if message is not None:
            self._apply_message(message)

    def _apply_message(self, message: InvalidationMessage) -> None:
        if message.action == "remove" and message.key is not None:
            remove_local = self._remove_local
            if remove_local is not None:
                remove_local(message.key)
            return

        if message.action == "clear":
            clear_local = self._clear_local
            if clear_local is not None:
                clear_local()

    def _encode_message(self, message: InvalidationMessage) -> str:
        payload: dict[str, str] = {
            "action": message.action,
            "source_id": self._source_id,
        }

        if message.key is not None:
            payload["key"] = message.key

        return json.dumps(payload, separators=(",", ":"))

    def _decode_message(self, payload: str) -> InvalidationMessage | None:
        try:
            data = json.loads(payload)
        except (TypeError, ValueError):
            return None

        if not isinstance(data, dict) or data.get("source_id") == self._source_id:
            return None

        if data.get("action") == "remove" and isinstance(data.get("key"), str):
            return InvalidationMessage.remove(data["key"])

        if data.get("action") == "clear":
            return InvalidationMessage.clear()

        return None
