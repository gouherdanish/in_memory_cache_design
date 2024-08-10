import os, json
from abc import ABC, abstractmethod

from constants import PathConstants
from cache_entry import CacheEntry

class PersistanceFactory:
    registry = {}

    @classmethod
    def get_manager(cls,id,**kwargs):
        try:
            return cls.registry[id](**kwargs)
        except:
            raise ValueError(f'Invalid Persistance Requested: {id}')
        
    @classmethod
    def register_manager(cls,id):
        def wrapper(wrapped_class):
            cls.registry[id] = wrapped_class
            return wrapped_class
        return wrapper
    
class PersistanceManager(ABC):
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self):
        pass

@PersistanceFactory.register_manager('json')
class JsonPersistance(PersistanceManager):
    def __init__(self) -> None:
        self.file_path = os.path.join(PathConstants.PERSISTANCE_DIR,'cache.json')
    
    def load(self):
        """
        Loads the persisted file from disk volume into memory
        """
        if os.path.exists(self.file_path):
            with open(self.file_path,'r') as f:
                data = json.load(f)
            return {k:CacheEntry(v['value'],v['expiration']) for k,v in data.items()}
        return {}
    
    def save(self,cache):
        """
        Persists the cached data onto disk
        """
        data = {k:{'value':v.value,'expiration':v.expiration} for k,v in cache.items()}
        with open(self.file_path,'w') as f:
            json.dump(data,f)