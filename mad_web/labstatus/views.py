from django.conf import settings
from django.shortcuts import render

from mad_web.labstatus.models import UTCSBackend, UTCSService


def main_app(request):
    backend = UTCSBackend(settings.UTCS_API_KEY)
    labs_data = backend.request(UTCSService.Labs)
    labs_layout_data = backend.request(UTCSService.LabsLayout)

    for name, coords in labs_layout_data.machines_layout[0].items():
        machine = labs_data.machines[0].get(name)
        if machine:
            machine.location = coords

    return render(request, 'labstatus/main.html', {"labs": labs_data.machines})
