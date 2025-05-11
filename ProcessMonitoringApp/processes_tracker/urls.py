from django.urls import path

from ProcessMonitoringApp.processes_tracker.views import RunningProcessesAPIView, index, AnomalyAlertsAPIView

urlpatterns = (
    path('', index, name='index'),
    path('api/processes/', RunningProcessesAPIView.as_view()),
    path('api/anomalies/', AnomalyAlertsAPIView.as_view()),
)
