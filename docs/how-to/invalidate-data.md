# Invalidate Cached Data

Invalidate cached data when your application changes the source record or when an operator needs to force a refresh.

```mermaid
flowchart TD
    Change["Source data changes"] --> Remove["Remove cached key"]
    Remove --> Local["Delete local L1 value"]
    Remove --> Distributed["Delete distributed L2 value"]
    Remove --> Notify["Notify peer instances"]
    Notify --> Peers["Peers drop local L1 value"]
```

## Remove one key

```python
await cache.remove("user:123")
```

This removes the key from local memory, deletes it from distributed storage when configured, and publishes an invalidation message when an invalidation bus is configured.

## Remove the key for a cached function call

```python
await get_user.remove_cached("123")
```

Use this when you decorated the read path and want to invalidate using the same arguments.

## Invalidate from inside application functions

You can invalidate cached data from inside any async function by calling the cache
or decorated function helper:

```python
@cache.cached(lambda user_id: f"user:{user_id}")
async def get_user(user_id: str) -> dict[str, str]:
    ...


async def update_user(user_id: str, data: dict[str, str]) -> None:
    await save_user(user_id, data)
    await get_user.remove_cached(user_id)
```

This is most useful from write paths that change the source data.

Avoid using `remove_cached()` inside the same cached function to keep that
function's current return value out of the cache. The decorator stores the
function result after the function returns, so removing the key during the
function body is followed by caching the returned value.

## Clear local memory and peer instances

```python
await cache.clear()
```

`clear()` clears the current process and publishes a clear message to peer instances. It does not delete every key from a distributed cache.

## Remove only this process's local copy

```python
cache.remove_local("user:123")
cache.clear_memory()
```

Use local-only operations for application-specific recovery paths where you do not want to notify other instances.
