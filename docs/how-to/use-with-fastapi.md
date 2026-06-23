# Use With FastAPI

Use one `CacheSync` instance for the FastAPI application and start or stop it
from the application lifespan.

## Cache a service function

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from cache_sync import CacheOptions, CacheSync


cache = CacheSync(
    options=CacheOptions(
        ttl_seconds=60,
        fail_safe_seconds=300,
        max_keys=1_000,
    ),
)


@cache.cached(lambda user_id: f"user:{user_id}")
async def load_user(user_id: str) -> dict[str, str]:
    user = await fetch_user_from_database(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await cache.start()
    try:
        yield
    finally:
        await cache.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/users/{user_id}")
async def get_user(user_id: str) -> dict[str, str]:
    return await load_user(user_id)
```

!!! note "Use explicit keys for endpoints"

    Prefer caching a service function with an explicit key instead of decorating
    the FastAPI endpoint directly with the default generated key. Endpoint
    functions often receive request objects, dependency instances,
    authentication context, or other per-request values. If those values become
    part of the default key, the cache may miss more often than expected or
    cache data without the right tenant, user, locale, or permission boundary.

## Cache an endpoint function

You can also decorate an async FastAPI endpoint directly. Put the FastAPI route
decorator above `@cache.cached`, and use an explicit cache key:

```python
@app.get("/users/{user_id}")
@cache.cached(lambda user_id: f"user:{user_id}")
async def get_user(user_id: str) -> dict[str, str]:
    user = await fetch_user_from_database(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name}
```

This works best for simple endpoints whose response depends only on stable
path, query, or body values included in the key. For endpoints with request
objects, dependencies, authentication context, or other framework-specific
inputs, cache a service function instead.

## Invalidate after writes

Call `remove_cached` after the application changes the underlying record:

```python
@app.put("/users/{user_id}")
async def update_user(user_id: str, payload: UpdateUser) -> dict[str, str]:
    await save_user_to_database(user_id, payload)
    await load_user.remove_cached(user_id)
    return await load_user(user_id)
```

## Share cached values between FastAPI workers

Each FastAPI worker has its own local L1 cache. Add Redis when multiple workers
or application instances should share cached values:

```python
from redis.asyncio import Redis

from cache_sync import CacheOptions, CacheSync, RedisDistributedCache


redis = Redis.from_url("redis://localhost:6379/0")

cache = CacheSync(
    distributed_cache=RedisDistributedCache(redis),
    options=CacheOptions(ttl_seconds=60, fail_safe_seconds=300, max_keys=1_000),
)
```

Use an invalidation bus when writes in one worker should remove local L1 entries
from other workers before their TTL expires.
