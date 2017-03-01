from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from mad_web.labstatus.models import UTCSService, UTCSBackend


def main_app(request):
    return render(request, 'labstatus/main.html',
                  {"description": "See which machines are available in the UTCS labs"})


def backend_proxy(request):
    if not ("txcsmad.com/" in request.META["HTTP_REFERER"] or "0.0.0.0" in request.META["HTTP_REFERER"]):
        return HttpResponse({}, content_type='application/json')
    backend = UTCSBackend(settings.UTCS_API_KEY)
    service = request.GET.get('service')
    if service == "labs-layout":
        json = backend.raw_request(UTCSService.LabsLayout)
    else:
        json = backend.raw_request(UTCSService.Labs)
    return HttpResponse(json, content_type='application/json')
