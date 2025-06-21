import logging
import time
from functools import lru_cache
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class Cache:
    def __init__(self, max_size: int = 1000, ttl: int = 300):
        """
        Initialize cache.

        Args:
            max_size: Maximum number of items in cache
            ttl: Time-to-live in seconds for cached items
        """
        self.max_size = max_size
        self.ttl = ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_hits = 0
        self._cache_misses = 0

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get item from cache."""
        if key in self._cache:
            item = self._cache[key]
            if time.time() - item["timestamp"] <= self.ttl:
                self._cache_hits += 1
                return item["value"]
            else:
                # Remove expired item
                del self._cache[key]
        self._cache_misses += 1
        return None

    def set(self, key: str, value: Dict[str, Any]):
        """Set item in cache."""
        if len(self._cache) >= self.max_size:
            # Remove oldest item
            oldest_key = min(
                self._cache.keys(), key=lambda k: self._cache[k]["timestamp"]
            )
            del self._cache[oldest_key]

        self._cache[key] = {"value": value, "timestamp": time.time()}

    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "hits": self._cache_hits,
            "misses": self._cache_misses,
            "hit_rate": self._cache_hits / (self._cache_hits + self._cache_misses)
            if (self._cache_hits + self._cache_misses) > 0
            else 0,
            "current_size": len(self._cache),
            "max_size": self.max_size,
        }

    def clear(self):
        """Clear the cache."""
        self._cache.clear()
        self._cache_hits = 0
        self._cache_misses = 0


class MetricCache:
    def __init__(self, cache: Cache):
        self.cache = cache

    def get_metrics(self, source: str, metric: str) -> Optional[Dict[str, Any]]:
        """Get cached metrics for a specific source and metric."""
        key = f"metrics_{source}_{metric}"
        return self.cache.get(key)

    def set_metrics(self, source: str, metric: str, value: Dict[str, Any]):
        """Cache metrics for a specific source and metric."""
        key = f"metrics_{source}_{metric}"
        self.cache.set(key, value)

    def get_alerts(self, source: str, level: str) -> Optional[List[Dict[str, Any]]]:
        """Get cached alerts for a specific source and level."""
        key = f"alerts_{source}_{level}"
        return self.cache.get(key)

    def set_alerts(self, source: str, level: str, value: List[Dict[str, Any]]):
        """Cache alerts for a specific source and level."""
        key = f"alerts_{source}_{level}"
        self.cache.set(key, value)


# Decorator for caching function results
def cache_result(cache: Cache, key_func):
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = key_func(*args, **kwargs)
            result = cache.get(key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(key, result)
            return result

        return wrapper

    return decorator
