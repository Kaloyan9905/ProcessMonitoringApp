import threading

import psutil

from ProcessMonitoringApp.processes_tracker.anomaly_detection import monitor, CPU_THRESHOLD, MEMORY_THRESHOLD


class ProcessCollector:
    def __init__(self):
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

                    name = proc.info['name']
                    pid = proc.info['pid']
                    cpu = proc.info['cpu_percent']
                    mem = proc.info['memory_percent']

                    if cpu > CPU_THRESHOLD:
                        monitor.check_usage('cpu', pid, name, cpu)

                    if mem > MEMORY_THRESHOLD:
                        monitor.check_usage('memory', pid, name, mem)

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            with self._lock:
                self.data = processes

    def get_data(self):
        with self._lock:
            return list(self.data)


collector = ProcessCollector()
