import os, json

from constants import PathConstants
from cache_entry import CacheEntry

class JsonPersistance:
    def __init__(self,file_path) -> None:
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