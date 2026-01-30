"""Caching utilities for LLM responses."""

import hashlib
import json
import threading
import time
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Dict, Optional, Tuple

from .models import ChatResponse


@dataclass
class CacheEntry:
    """Entry in the response cache."""
    response: ChatResponse
    timestamp: float
    hits: int = 0


class ResponseCache:
    """Thread-safe in-memory cache for LLM responses."""
    
    def __init__(self, ttl: int = 3600, max_size: int = 1000):
        """
        Initialize response cache.
        
        Args:
            ttl: Time-to-live for cache entries in seconds
            max_size: Maximum number of entries to store
        """
        self.ttl = ttl
        self.max_size = max_size
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[ChatResponse]:
        """
        Get response from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached response if found and not expired, None otherwise
        """
        with self._lock:
            if key not in self._cache:
                return None
            
            entry = self._cache[key]
            
            # Check if expired
            if time.time() - entry.timestamp > self.ttl:
                del self._cache[key]
                return None
            
            # Update hit count
            entry.hits += 1
            return entry.response
    
    def set(self, key: str, response: ChatResponse) -> None:
        """
        Store response in cache.
        
        Args:
            key: Cache key
            response: Response to cache
        """
        with self._lock:
            # Evict oldest entry if cache is full
            if len(self._cache) >= self.max_size:
                oldest_key = min(
                    self._cache.keys(),
                    key=lambda k: self._cache[k].timestamp
                )
                del self._cache[oldest_key]
            
            self._cache[key] = CacheEntry(
                response=response,
                timestamp=time.time(),
                hits=0
            )
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        """
        with self._lock:
            total_hits = sum(entry.hits for entry in self._cache.values())
            return {
                "size": len(self._cache),
                "max_size": self.max_size,
                "total_hits": total_hits,
                "ttl": self.ttl,
            }


# Global cache instance
_global_cache = ResponseCache()


def generate_cache_key(
    model: str,
    messages: list,
    temperature: float,
    max_tokens: Optional[int] = None,
    **kwargs
) -> str:
    """
    Generate a unique cache key from request parameters.
    
    Args:
        model: Model name
        messages: List of messages
        temperature: Temperature parameter
        max_tokens: Maximum tokens
        **kwargs: Additional parameters
        
    Returns:
        SHA256 hash of the request parameters
    """
    # Convert messages to hashable format
    messages_str = json.dumps(
        [{"role": m.role, "content": m.content} if hasattr(m, "role") else m 
         for m in messages],
        sort_keys=True
    )
    
    # Include relevant parameters
    cache_data = {
        "model": model,
        "messages": messages_str,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    
    # Add any additional kwargs that affect the response
    for key in sorted(kwargs.keys()):
        if key not in ["stream", "extra_params"]:  # Skip non-deterministic params
            cache_data[key] = kwargs[key]
    
    # Generate hash
    cache_str = json.dumps(cache_data, sort_keys=True)
    return hashlib.sha256(cache_str.encode()).hexdigest()


def cache_response(
    ttl: int = 3600,
    cache_instance: Optional[ResponseCache] = None
):
    """
    Decorator to cache LLM responses.
    
    Args:
        ttl: Time-to-live for cache entries in seconds
        cache_instance: Optional cache instance (uses global cache if None)
        
    Returns:
        Decorated function
        
    Example:
        @cache_response(ttl=3600)
        def chat(self, request: ChatRequest) -> ChatResponse:
            return self.provider.chat_completion(request)
    """
    cache = cache_instance or _global_cache
    cache.ttl = ttl
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> ChatResponse:
            # Extract request parameters
            # Handle both ChatRequest object and individual parameters
            if args and hasattr(args[0], "model"):
                request = args[0]
                cache_key = generate_cache_key(
                    model=request.model,
                    messages=request.messages,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens,
                )
            else:
                cache_key = generate_cache_key(**kwargs)
            
            # Check cache
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                return cached_response
            
            # Execute function
            response = func(*args, **kwargs)
            
            # Cache response (only if not streaming)
            if not kwargs.get("stream", False):
                cache.set(cache_key, response)
            
            return response
        
        return wrapper
    return decorator


def get_cache_stats() -> Dict[str, Any]:
    """
    Get statistics from the global cache.
    
    Returns:
        Dictionary with cache statistics
    """
    return _global_cache.get_stats()


def clear_cache() -> None:
    """Clear the global cache."""
    _global_cache.clear()
