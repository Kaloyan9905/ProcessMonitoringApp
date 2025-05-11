import time

from plyer import notification
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Optional


class Notifier:
    @staticmethod
    def notify(title: str, message: str):
        notification.notify(
            title=title,
            message=message,
            timeout=5
        )


class UsageAlert(ABC):
    MAX_DATA_LENGTH = 25

    def __init__(self, threshold: float, notifier: Notifier, cooldown: int = 60):
        self.threshold = threshold
        self.notifier = notifier
        self.usage_data = defaultdict(list)
        self.last_alert_time = {}
        self.cooldown = cooldown

    def track(self, pid: int, name: str, usage: float) -> Optional[float]:
        self.usage_data[pid].append(usage)

        if len(self.usage_data[pid]) == self.MAX_DATA_LENGTH:
            if all(value > self.threshold for value in self.usage_data[pid]):
                now = time.time()
                last_time = self.last_alert_time.get(pid, 0)

                if now - last_time >= self.cooldown:
                    avg = sum(self.usage_data[pid]) / self.MAX_DATA_LENGTH

                    self.send_alert(pid, name, avg)
                    self.last_alert_time[pid] = now
                    self.usage_data[pid] = []

                    return avg

            self.usage_data[pid] = []

        return None

    @abstractmethod
    def send_alert(self, pid: int, name: str, average_usage: float):
        pass


class CPUUsageAlert(UsageAlert):
    def send_alert(self, pid: int, name: str, average_usage: float):
        self.notifier.notify(
            'High CPU Usage',
            f'{name} (PID {pid}) average CPU usage: {average_usage:.2f}%'
        )


class MemoryUsageAlert(UsageAlert):
    def send_alert(self, pid: int, name: str, average_usage: float):
        self.notifier.notify(
            'High Memory Usage',
            f'{name} (PID {pid}) average memory usage: {average_usage:.2f}%'
        )


class ResourceMonitor:
    def __init__(self, alerts: list[UsageAlert]):
        self.alerts = alerts

    def check_usage(self, usage_type: str, pid: int, name: str, usage: float) -> Optional[float]:
        for alert in self.alerts:
            if isinstance(alert, CPUUsageAlert) and usage_type == 'cpu':
                return alert.track(pid, name, usage)
            elif isinstance(alert, MemoryUsageAlert) and usage_type == 'memory':
                return alert.track(pid, name, usage)

        return None


CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 50

notifier = Notifier()
cpu_alert = CPUUsageAlert(threshold=CPU_THRESHOLD, notifier=notifier)
memory_alert = MemoryUsageAlert(threshold=MEMORY_THRESHOLD, notifier=notifier)

monitor = ResourceMonitor(alerts=[cpu_alert, memory_alert])
