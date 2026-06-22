# Cache Options

`CacheOptions` controls freshness, stale fallback, factory timeout, and TTL jitter.

| Option | Type | Default | Meaning |
| --- | --- | --- | --- |
| `ttl_seconds` | `float` | `60` | Fresh lifetime for values in local memory and distributed storage |
| `fail_safe_seconds` | `float` | `300` | Extra time a stale local value can be returned after a refresh error |
| `hard_timeout_seconds` | `float` | `5` | Maximum time to wait for the value factory |
| `jitter_seconds` | `float` | `0` | Random extra seconds added to the TTL |

Pass options to the cache for global defaults:

```python
cache = CacheSync(options=CacheOptions(ttl_seconds=120))
```

Pass options to `@cache.cached` for one function:

```python
@cache.cached(options=CacheOptions(ttl_seconds=30))
async def load_value() -> str:
    ...
```
