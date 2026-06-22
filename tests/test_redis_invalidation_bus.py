from __future__ import annotations

from typing import Any, cast

from cache_sync import RedisStreamsInvalidationBus


class FakeRedis:
    def __init__(self) -> None:
        self.added: list[tuple[str, dict[Any, Any], int | None, bool]] = []
        self.acked: list[tuple[str, str, bytes | str]] = []

    async def xadd(
        self,
        stream_name: str,
        fields: dict[Any, Any],
        *,
        maxlen: int | None = None,
        approximate: bool = False,
    ) -> None:
        self.added.append((stream_name, fields, maxlen, approximate))

    async def xack(
        self,
        stream_name: str,
        group_name: str,
        message_id: bytes | str,
    ) -> None:
        self.acked.append((stream_name, group_name, message_id))


async def test_redis_streams_invalidation_bus_publishes_invalidations() -> None:
    redis = FakeRedis()
    bus = RedisStreamsInvalidationBus(
        cast(Any, redis),
        stream_name="invalidations",
        max_length=50,
    )

    await bus.invalidate("user:1")
    await bus.clear()

    assert redis.added[0][0] == "invalidations"
    assert redis.added[0][1]["action"] == "remove"
    assert redis.added[0][1]["key"] == "user:1"
    assert redis.added[0][2:] == (50, True)
    assert redis.added[1][1]["action"] == "clear"


async def test_redis_streams_invalidation_bus_applies_remote_messages() -> None:
    redis = FakeRedis()
    bus = RedisStreamsInvalidationBus(
        cast(Any, redis),
        stream_name="invalidations",
        node_name="node",
    )
    removed: list[str] = []
    clear_count = 0

    def clear_local() -> None:
        nonlocal clear_count
        clear_count += 1

    bus._remove_local = removed.append
    bus._clear_local = clear_local
    await bus._process_message(
        "1-0",
        {
            "action": "remove",
            "source_id": "another-node",
            "key": "user:1",
        },
    )
    await bus._process_message(
        "2-0",
        {
            "action": "clear",
            "source_id": "another-node",
        },
    )

    assert removed == ["user:1"]
    assert clear_count == 1
    assert redis.acked == [
        ("invalidations", "cache-sync-node:node", "1-0"),
        ("invalidations", "cache-sync-node:node", "2-0"),
    ]
