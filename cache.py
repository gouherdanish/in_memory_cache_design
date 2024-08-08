import random
import time
import threading

from storage_manager import StorageFactory
from cache_entry import CacheEntry
from expiration_manager import ExpirationManager

class ThreadSafeCache:
    """
    Features 
    - Uses lock to make thread safe updates
    - Uses LRU policy for capacity management
    - Implements Expiration Policy on Cache Keys
        - Uses a parallel daemon thread running every 5 second
    """
    def __init__(
            self,
            capacity=5,
            cleanup_interval=5,
            eviction_policy='lru'
        ) -> None:
        self._capacity = capacity
        self._cleanup_interval = cleanup_interval
        self._lock = threading.Lock()
        self._storage = StorageFactory.get_manager(eviction_policy,capacity=capacity)
        self._expiration_manager = ExpirationManager()
        self._expiration_manager.track(self._periodic_cleanup)
    
    def get(self,key):
        with self._lock:
            entry = self._storage.get(key)
            if entry is not None:
                if not entry.is_expired(): return entry.value
                else: self._storage.delete(key)
            return None

    def set(self,key,val,ttl=None):
        with self._lock:
            entry = CacheEntry(val,ttl)
            self._storage.put(key,entry)

    def clear(self):
        with self._lock:
            self._storage.clear_expired()

    def stop(self):
        self._expiration_manager.stop()

    def _periodic_cleanup(self):
        while not self._expiration_manager._stop_cleanup_event.is_set():
            self._expiration_manager.sleep(interval=self._cleanup_interval)
            self.clear()


if __name__=='__main__':
    cache = ThreadSafeCache(capacity=5,cleanup_interval=3)
    print(cache._storage)

    # Caching some entries 
    cache.set('apple',100,ttl=3)
    print(cache._storage)

    cache.set('orange',80,ttl=7)
    print(cache._storage)

    # Wait for apple to expire
    time.sleep(4)
    print(cache._storage)

    cache.set('apple',150)
    print(cache._storage)

    cache.set('mango',120,ttl=14)
    print(cache._storage)
    
    # Run for a while to see periodic cleanup in action
    time.sleep(10)
    print(cache._storage)

    # Stop the cleanup thread properly
    cache.stop()  



