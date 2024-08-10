from abc import ABC, abstractmethod
import threading
import time

class WorkerFactory:
    registry = {}

    @classmethod
    def register_worker(cls,how):
        def wrap_fn(wrapped_cls):
            cls.registry[how] = wrapped_cls
            return wrapped_cls
        return wrap_fn
    
    @classmethod
    def get_worker(cls,how,**kwargs):
        print(how,kwargs)
        try:
            return cls.registry[how](**kwargs)
        except:
            raise ValueError(f'Invalid Worker Requested: {how}')

class Worker(ABC):
    def __init__(self) -> None:
        self._stop_event = threading.Event()

    def start(self,target):
        self._thread = threading.Thread(target=target, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()

    def pause(self,interval):
        print(f'Thread going to sleep for {interval} s')
        time.sleep(interval)

@WorkerFactory.register_worker('cleanup')
class CleanupWorker(Worker):
    pass

@WorkerFactory.register_worker('persistance')
class PersistanceWorker(Worker):
    pass

