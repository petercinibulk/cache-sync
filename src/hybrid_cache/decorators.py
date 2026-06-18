from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable
from typing import Any, Generic, ParamSpec, TypeVar

from hybrid_cache.core import CacheOptions, HybridCache

P = ParamSpec("P")
T = TypeVar("T")


class CachedFunction(Generic[P, T]):
    def __init__(
        self,
        cache: HybridCache,
        func: Callable[P, Awaitable[T]],
        key: str | Callable[..., str] | None,
        options: CacheOptions | None,
    ) -> None:
        self._cache = cache
        self._func = func
        self._key = key
        self._options = options

    async def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return await self._cache.get_or_set(
            self.cache_key(*args, **kwargs),
            lambda: self._func(*args, **kwargs),
            options=self._options,
        )

    async def remove_cached(self, *args: P.args, **kwargs: P.kwargs) -> None:
        await self._cache.remove(self.cache_key(*args, **kwargs))

    def cache_key(self, *args: P.args, **kwargs: P.kwargs) -> str:
        if isinstance(self._key, str):
            return self._key
        if self._key is None:
            return default_cache_key(self._func, *args, **kwargs)
        return self._key(*args, **kwargs)


def cached(
    cache: HybridCache,
    key: str | Callable[..., str] | None = None,
    *,
    options: CacheOptions | None = None,
) -> Callable[[Callable[P, Awaitable[T]]], CachedFunction[P, T]]:
    def decorator(func: Callable[P, Awaitable[T]]) -> CachedFunction[P, T]:
        return CachedFunction(cache, func, key, options)

    return decorator


def default_cache_key(func: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any) -> str:
    signature = inspect.signature(func)
    bound = signature.bind(*args, **kwargs)
    bound.apply_defaults()
    arguments = ",".join(
        f"{name}={_stable_key_part(value)}" for name, value in bound.arguments.items()
    )
    module = getattr(func, "__module__", type(func).__module__)
    qualname = getattr(func, "__qualname__", type(func).__qualname__)

    return f"{module}.{qualname}({arguments})"


def _stable_key_part(value: Any) -> str:
    if isinstance(value, dict):
        items = sorted(
            (_stable_key_part(key), _stable_key_part(item_value))
            for key, item_value in value.items()
        )
        return "{" + ",".join(f"{key}:{item_value}" for key, item_value in items) + "}"

    if isinstance(value, (list, tuple)):
        opener, closer = ("[", "]") if isinstance(value, list) else ("(", ")")
        return opener + ",".join(_stable_key_part(item) for item in value) + closer

    if isinstance(value, (set, frozenset)):
        items = sorted(_stable_key_part(item) for item in value)
        return "{" + ",".join(items) + "}"

    return repr(value)
