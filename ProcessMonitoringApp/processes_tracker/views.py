from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render

from ProcessMonitoringApp.processes_tracker.process_collector import collector


class RunningProcessesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        sort_key = request.GET.get('sort', 'pid')
        sort_order = request.GET.get('order', 'asc')
        filter_name = request.GET.get('filter', '').lower()

        processes = collector.get_data()

        if filter_name:
            processes = [p for p in processes if filter_name in p['name'].lower()]

        reverse = sort_order == 'desc'

        try:
            processes.sort(key=lambda x: x.get(sort_key, 0), reverse=reverse)
        except KeyError:
            pass

        return Response(processes)


def index(request):
    return render(request, 'index.html')
