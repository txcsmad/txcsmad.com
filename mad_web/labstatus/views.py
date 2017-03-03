import json
import os
from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from mad_web.labstatus.cron_tasks import ArchiveLabsResponse
from mad_web.labstatus.models import UTCSService, UTCSBackend, LabsResponse


def main_app(request):
    return render(request, 'labstatus/main.html',
                  {"description": "See which machines are available in the UTCS labs"})


def backend_proxy(request):
    backend = UTCSBackend(settings.UTCS_API_KEY)
    service = request.GET.get('service')
    if service == "labs-layout":
        json = backend.raw_request(UTCSService.LabsLayout)
    else:
        json = backend.raw_request(UTCSService.Labs)
    return HttpResponse(json, content_type='application/json')


def last_day_occupied_stats(request):
    current_time = datetime.now()
    day_ago = current_time - timedelta(days=1)
    paths = ArchiveLabsResponse.response_paths_for_datetime_window(day_ago, current_time)
    stats = [[], []]
    for path in paths:
        if not os.path.isfile(path):
            continue
        with open(path) as file:
            raw_string = file.read()
            data = json.loads(raw_string)
            parsed = LabsResponse(data)
            stat = parsed.num_occupied_by_lab()
            stats[0].append(stat[0])
            stats[1].append(stat[1])

    return HttpResponse(json.dumps(stats), content_type='application/json')
