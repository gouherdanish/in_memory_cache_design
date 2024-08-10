import random
import time
import threading

from cache_entry import CacheEntry
from factory.storage_factory import StorageFactory
from factory.worker_factory import CleanupWorker, PersistanceWorker
from factory.persistance_factory import PersistanceFactory

class ThreadSafeCache:
    """
    Features 
    - Uses lock to make thread safe updates
    - Uses LRU policy for capacity management
    - Implements Expiration Policy on Cache Keys and cleans up expired entries using a background thread
    - Persists the cached data to disk periodically 
    """
    def __init__(
            self,
            capacity=5,
            eviction_policy='lru',
            cleanup_interval=5,
            persistance_type='json'
        ) -> None:
        self._capacity = capacity
        self._cleanup_interval = cleanup_interval
        self._lock = threading.Lock()
        self._storage = StorageFactory.get_manager(eviction_policy,capacity=capacity)
        self._persistance = PersistanceFactory.get_manager(persistance_type)
        self.__start_workers__()

    def __start_workers__(self):
        self._storage_cleanup_worker = CleanupWorker()
        self._storage_cleanup_worker.start(self._periodic_cleanup)
        
        self._persistance_worker = PersistanceWorker()
        self._persistance_worker.start(self._periodic_save)
    
    def get(self,key):
        with self._lock:
            entry = self._storage.get(key)
            if entry is not None:
                if not entry.is_expired(): return entry.value
                else: self._storage.delete(key)
            return None

    def set(self,key,val,expiration=None):
        with self._lock:
            entry = CacheEntry(val,expiration)
            self._storage.put(key,entry)

    def clear(self):
        with self._lock:
            self._storage.clear_expired()

    def persist(self):
        with self._lock:
            self._persistance.save(self._storage._cache)

    def stop(self):
        self._storage_cleanup_worker.stop()

    def _periodic_cleanup(self):
        while not self._storage_cleanup_worker._stop_event.is_set():
            self._storage_cleanup_worker.pause(interval=self._cleanup_interval)
            self.clear()

    def _periodic_save(self):
        while not self._persistance_worker._stop_event.is_set():
            self._persistance_worker.pause(interval=self._cleanup_interval)
            self.persist()

if __name__=='__main__':
    cache = ThreadSafeCache(capacity=5,cleanup_interval=3)
    print(cache._storage)

    # Caching some entries 
    cache.set('apple',100,expiration=3)
    print(cache._storage)

    cache.set('orange',80,expiration=7)
    print(cache._storage)

    # Wait for apple to expire
    time.sleep(4)
    print(cache._storage)

    cache.set('apple',150)
    print(cache._storage)

    cache.set('mango',120,expiration=14)
    print(cache._storage)
    
    # Run for a while to see periodic cleanup in action
    time.sleep(10)
    print(cache._storage)

    # Stop the cleanup thread properly
    cache.stop()  



