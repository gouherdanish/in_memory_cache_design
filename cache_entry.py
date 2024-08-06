import time

class CacheEntry:
    def __init__(self,value,expiration) -> None:
        self.value = value
        self.expiration = expiration

    def __str__(self) -> str:
        return f'{self.value}'
    
    def __repr__(self) -> str:
        return str(self)

    def is_expired(self):
        return self.expiration and self.expiration < time.time()