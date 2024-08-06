import time

class CacheEntry:
    def __init__(self,value,ttl) -> None:
        self.value = value
        self.ttl = ttl
        self.expiration = time.time() + ttl if ttl else None

    def __str__(self) -> str:
        return f'{self.value} ({self.ttl}s)' if self.ttl else f'{self.value}'
    
    def __repr__(self) -> str:
        return str(self)

    def is_expired(self):
        return self.expiration and self.expiration < time.time()