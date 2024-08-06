import threading
from storage import LRUCache

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

