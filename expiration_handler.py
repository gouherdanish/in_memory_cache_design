import threading

class ExpirationHandler:
    def __init__(self) -> None:
        self._stop_cleanup_event = threading.Event()

    def track(self,target):
        self._cleanup_thread = threading.Thread(target=target, daemon=True)
        self._cleanup_thread.start()

    def stop(self):
        self._stop_cleanup_event.set()
        self._cleanup_thread.join()