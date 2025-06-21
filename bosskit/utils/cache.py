import hashlib
import json
import os
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional, Union


class Cache:
    def __init__(
        self,
        cache_dir: str = None,
        ttl: int = 3600,
        max_size: int = 100000000  # 100MB
    ):
        """Initialize the cache.

        Args:
            cache_dir: Directory to store cache files
            ttl: Time-to-live in seconds
            max_size: Maximum cache size in bytes
        """
        self.cache_dir = Path(cache_dir or os.path.expanduser('~/.bosskit/cache'))
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl
        self.max_size = max_size

    def _get_cache_key(self, func: Callable, *args, **kwargs) -> str:
        """Generate a unique cache key.

        Args:
            func: Function being called
            args: Function arguments
            kwargs: Function keyword arguments

        Returns:
            Unique cache key
        """
        key = f"{func.__module__}.{func.__name__}" + \
              json.dumps(args, sort_keys=True) + \
              json.dumps(kwargs, sort_keys=True)
        return hashlib.sha256(key.encode()).hexdigest()

    def _get_cache_file(self, key: str) -> Path:
        """Get cache file path.

        Args:
            key: Cache key

        Returns:
            Path to cache file
        """
        return self.cache_dir / f"{key}.cache"

    def _is_expired(self, cache_file: Path) -> bool:
        """Check if cache file is expired.

        Args:
            cache_file: Path to cache file

        Returns:
            True if cache is expired, False otherwise
        """
        if not cache_file.exists():
            return True

        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        return (datetime.now() - mtime).total_seconds() > self.ttl

    def _get_cache_size(self) -> int:
        """Get total cache size in bytes.

        Returns:
            Total cache size in bytes
        """
        return sum(f.stat().st_size for f in self.cache_dir.glob('*.cache'))

    def _cleanup(self):
        """Clean up expired and excess cache entries."""
        # Remove expired entries
        for cache_file in self.cache_dir.glob('*.cache'):
            if self._is_expired(cache_file):
                cache_file.unlink()

        # Remove excess entries if cache is too large
        while self._get_cache_size() > self.max_size:
            oldest_file = min(
                self.cache_dir.glob('*.cache'),
                key=lambda f: f.stat().st_mtime
            )
            oldest_file.unlink()

    def cache(self, ttl: Optional[int] = None):
        """Decorator to cache function results.

        Args:
            ttl: Time-to-live in seconds (overrides default)

        Returns:
            Decorated function
        """
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                key = self._get_cache_key(func, *args, **kwargs)
                cache_file = self._get_cache_file(key)

                # Check cache
                if cache_file.exists() and not self._is_expired(cache_file):
                    try:
                        with open(cache_file, 'r') as f:
                            data = json.load(f)
                            return data['result']
                    except Exception:
                        pass

                # Execute function and cache result
                result = func(*args, **kwargs)

                try:
                    cache_data = {
                        'timestamp': datetime.now().isoformat(),
                        'result': result
                    }
                    with open(cache_file, 'w') as f:
                        json.dump(cache_data, f)

                    self._cleanup()
                    return result
                except Exception:
                    return result

            return wrapper

        if callable(ttl):
            return decorator(ttl)
        return decorator

def cache(
    ttl: Union[int, Callable] = 3600,
    cache_dir: Optional[str] = None,
    max_size: int = 100000000
):
    """Cache decorator factory.

    Args:
        ttl: Time-to-live in seconds
        cache_dir: Directory to store cache files
        max_size: Maximum cache size in bytes

    Returns:
        Cache decorator
    """
    cache_instance = Cache(cache_dir=cache_dir, ttl=ttl, max_size=max_size)

    if callable(ttl):
        return cache_instance.cache()(ttl)
    return cache_instance.cache(ttl)

def invalidate_cache(cache_key: str, cache_dir: Optional[str] = None) -> None:
    """Invalidate a specific cache entry.

    Args:
        cache_key: Cache key to invalidate
        cache_dir: Cache directory
    """
    cache_file = Path(cache_dir or os.path.expanduser('~/.bosskit/cache')) / f"{cache_key}.cache"
    if cache_file.exists():
        cache_file.unlink()

def clear_cache(cache_dir: Optional[str] = None) -> None:
    """Clear all cache entries.

    Args:
        cache_dir: Cache directory
    """
    cache_dir = Path(cache_dir or os.path.expanduser('~/.bosskit/cache'))
    for cache_file in cache_dir.glob('*.cache'):
        cache_file.unlink()
