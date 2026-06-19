# Decorator Behavior

`cache.cached(key=None, *, options=None)` wraps an async function and returns a callable object with cache helpers.

## Key behavior

| Key setting | Behavior |
| --- | --- |
| Omitted | Builds a key from function module, qualified name, and bound arguments |
| String | Uses the same fixed key for every call |
| Callable | Calls the function with the same arguments and uses the returned string |

## Helper methods

| Method | Behavior |
| --- | --- |
| `await cached_function(...)` | Returns a cached value or calls the wrapped async function |
| `await cached_function.remove_cached(...)` | Removes the cached value for those arguments |
| `cached_function.cache_key(...)` | Returns the key for those arguments |

## Default key shape

Default keys include the function module, qualified name, and arguments. For stable operational keys, prefer an explicit callable:

```python
@cache.cached(lambda user_id: f"user:{user_id}")
async def get_user(user_id: str) -> dict[str, str]:
    ...
```
