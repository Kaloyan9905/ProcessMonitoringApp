import threading
import psutil
import time


class ProcessCollector:
    def __init__(self, interval=2):
        self.interval = interval
        self.data = []
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._update_loop, daemon=True)
        self._thread.start()

    def _update_loop(self):
        while True:
            processes = []

            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            with self._lock:
                self.data = processes

            time.sleep(self.interval)

    def get_data(self):
        with self._lock:
            return list(self.data)


collector = ProcessCollector(interval=2)
