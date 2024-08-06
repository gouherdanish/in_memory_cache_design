import time
import threading

from storage import LRUCache
from cache_entry import CacheEntry
from expiration_handler import ExpirationHandler

class ThreadSafeCache:
    """
    Features 
    - Uses lock to make thread safe updates
    - Uses LRU policy for capacity management
    - Implements Expiration Policy on Cache Keys
        - Uses a parallel daemon thread running every 1 second
    """
    def __init__(self,capacity,cleanup_interval) -> None:
        self._capacity = capacity
        self._cleanup_interval = cleanup_interval
        self._storage = LRUCache(capacity)
        self._lock = threading.Lock()
        self._expiration_handler = ExpirationHandler()
        self._expiration_handler.track(self._periodic_cleanup)
    
    def get(self,key):
        with self._lock:
            entry = self._storage.get(key)
            if entry is not None:
                if not entry.is_expired(): return entry.value
                else: self._storage.delete(key)
            return None

    def set(self,key,val,expires_in=None):
        print(key,val,expires_in)
        with self._lock:
            print(key,val,expires_in,time.time())
            expiration = time.time() + expires_in if expires_in else None
            print(expiration)
            entry = CacheEntry(val,expiration)
            self._storage.put(key,entry)

    def stop(self):
        self._expiration_handler.stop()

    def _periodic_cleanup(self):
        while not self._expiration_handler._stop_cleanup_event.is_set():
            print(f'Sleeping with Daemon for {self._cleanup_interval} s')
            time.sleep(self._cleanup_interval)
            self._cleanup_expired()

    def _cleanup_expired(self):
        with self._lock:
            for key,entry in self._storage._cache.items():
                if entry.is_expired():
                    self._storage.delete(key)

if __name__=='__main__':
    cache = ThreadSafeCache(capacity=5,cleanup_interval=5)
    print(cache._storage)

    cache.set('apple',100,expires_in=3)
    print(cache._storage)

    cache.set('orange',80,expires_in=7)
    print(cache._storage)

    print('SLEEPING for 4')
    time.sleep(4)
    print(cache.get('apple'))

    cache.set('apple',150)
    print(cache._storage)

    cache.set('mango',120,expires_in=4)
    print(cache._storage)
    
    # Run for a while to see periodic cleanup in action
    time.sleep(10)
    cache.stop()  # Stop the cleanup thread properly



