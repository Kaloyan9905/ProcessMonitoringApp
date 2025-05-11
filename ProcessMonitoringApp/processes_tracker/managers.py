from typing import List, Dict


class AlertManager:
    def __init__(self):
        self.alerts: List[Dict] = []

    def notify(self, title: str, message: str, pid: int, name: str, usage: float):
        self.alerts.append({
            'title': title,
            'message': message,
            'pid': pid,
            'name': name,
            'usage': usage
        })

    def get_recent_alerts(self):
        recent = self.alerts[:]
        self.alerts.clear()
        return recent
