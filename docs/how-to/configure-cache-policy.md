# Configure Cache Policy

Cache policy controls freshness, stale fallback, timeout behavior, and TTL spread.

## Set defaults for the whole cache

```python
from hybrid_cache import CacheOptions, HybridCache

cache = HybridCache(
    options=CacheOptions(
        ttl_seconds=120,
        fail_safe_seconds=600,
        hard_timeout_seconds=3,
        jitter_seconds=10,
    ),
)
```

## Override policy for one cached function

```python
from hybrid_cache import CacheOptions, cached


@cached(
    cache,
    lambda product_id: f"product:{product_id}",
    options=CacheOptions(ttl_seconds=30, fail_safe_seconds=300),
)
async def get_product(product_id: str) -> dict[str, str]:
    ...
```

## Choose practical values

| Option | Use it for | Common starting point |
| --- | --- | --- |
| `ttl_seconds` | How long a value is fresh | 30 to 300 seconds |
| `fail_safe_seconds` | How long stale data can be used after a refresh error | 5 to 10 times the TTL |
| `hard_timeout_seconds` | Maximum time to wait for the value factory | Smaller than your request timeout |
| `jitter_seconds` | Spreading expirations across time | 5 to 10 percent of the TTL |

Use lower TTLs for frequently changing data. Use higher TTLs for expensive values that can be slightly out of date.
