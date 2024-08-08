from abc import ABC, abstractmethod
import threading
import time

class CleanupFactory:
    registry = {}

    @classmethod
    def register_manager(cls,how):
        def wrap_fn(wrapped_cls):
            cls.registry[how] = wrapped_cls
            return wrapped_cls
        return wrap_fn
    
    @classmethod
    def get_manager(cls,how,**kwargs):
        print(how,kwargs)
        try:
            return cls.registry[how](**kwargs)
        except:
            raise ValueError(f'Invalid Cleanup Requested: {how}')

class CleanupManager(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def pause(self):
        pass

@CleanupFactory.register_manager('background')
class BackgroundThreadCleanup(CleanupManager):
    def __init__(self) -> None:
        self._stop_cleanup_event = threading.Event()

    def start(self,target):
        self._cleanup_thread = threading.Thread(target=target, daemon=True)
        self._cleanup_thread.start()

    def stop(self):
        self._stop_cleanup_event.set()
        self._cleanup_thread.join()

    def pause(self,interval):
        print(f'Thread going to sleep for {interval} s')
        time.sleep(interval)