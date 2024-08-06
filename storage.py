
class LRUCache:
    """
    Implements Least Recently Used Cache Eviction Policy
    Uses Ordered Dict (sorted in insertion order)
    """
    def __init__(self,capacity) -> None:
        self._capacity = capacity
        self._cache = {}
    
    def __str__(self) -> str:
        return f'LRU({self._cache})'

    def __repr__(self):
        return str(self)
    
    def put(self,key,val):
        if key in self._cache:
            self._cache.pop(key)
        if len(self._cache) >= self._capacity:
            self._cache.pop(next(iter(self._cache)))
        self._cache[key] = val

    def get(self,key):
        if key in self._cache:
            val = self._cache.pop(key)
            self._cache[key] = val
            return val
        return None
    
    def delete(self,key):
        if key in self._cache:
            del self._cache[key]

    def clear_expired(self):
        expired_keys = [key for key,val in self._cache.items() if val.is_expired()]
        for key in expired_keys:
            del self._cache[key]