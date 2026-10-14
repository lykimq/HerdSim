"""Generic id -> factory registry shared by plugins, metrics, and scenarios."""

from __future__ import annotations

from collections.abc import Callable
from typing import Generic, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    """Map string ids to factories; ``get`` returns a fresh instance."""

    def __init__(self, kind: str):
        self.kind = kind
        self._factories: dict[str, Callable[[], T]] = {}

    def register(self, plugin_id: str, factory: Callable[[], T]) -> None:
        self._factories[plugin_id] = factory

    def get(self, plugin_id: str) -> T:
        if plugin_id not in self._factories:
            available = list(self._factories)
            raise KeyError(f"Unknown {self.kind} '{plugin_id}'. Available: {available}")
        return self._factories[plugin_id]()

    def get_all(self) -> list[T]:
        """Fresh instances of every registered plugin, in registration order."""
        return [factory() for factory in self._factories.values()]
