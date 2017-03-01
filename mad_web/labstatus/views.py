from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from mad_web.labstatus.models import UTCSService, UTCSBackend


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
