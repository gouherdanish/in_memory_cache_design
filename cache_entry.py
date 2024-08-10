import time

class CacheEntry:
    def __init__(self,value,expiration) -> None:
        self.value = value
        self.expiration = expiration
        self.expiration_epoch = time.time() + expiration if expiration else None

    def __str__(self) -> str:
        return f'{self.value} ({self.expiration}s)' if self.expiration else f'{self.value}'
    
    def __repr__(self) -> str:
        return str(self)

    def is_expired(self):
        return self.expiration_epoch and self.expiration_epoch < time.time()