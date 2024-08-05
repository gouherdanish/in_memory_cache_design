import threading

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

class ThreadSafeCache:
    """
    Features 
    - Uses lock to make thread safe updates
    - Uses LRU policy for capacity management
    """
    def __init__(self,capacity) -> None:
        self._storage = LRUCache(capacity)
        self._lock = threading.Lock()
    
    def get(self,key):
        with self._lock:
            self._storage.get(key)

    def set(self,key,val):
        with self._lock:
            self._storage.put(key,val)

if __name__=='__main__':
    c = ThreadSafeCache(2)
    c.set('apple',100)
    print(c._storage)

    c.set('orange',80)
    print(c._storage)

    c.set('apple',150)
    print(c._storage)

    c.set('mango',120)
    print(c._storage)

