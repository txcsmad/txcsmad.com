from django.conf import settings
from django.shortcuts import render

from mad_web.labstatus.models import UTCSBackend, UTCSService, LabsResponse, LabsLayoutResponse


def serialize_for_view(labs_data: LabsResponse, labs_layout_data: LabsLayoutResponse):
    serialized_labs = []
    machines = {**labs_data.machines[0], **labs_data.machines[1]}
    for lab in labs_layout_data.machines_layout:
        serialized_lab = []
        for name, coords in lab.items():
            machine = machines.get(name)
            if machine:
                machine.location = coords
                serialized_lab.append(machine.__dict__)
        serialized_labs.append(serialized_lab)
    return serialized_labs


def main_app(request):
    backend = UTCSBackend(settings.UTCS_API_KEY)
    labs_data = backend.request(UTCSService.Labs)
    labs_layout_data = backend.request(UTCSService.LabsLayout)

    labs = serialize_for_view(labs_data, labs_layout_data)

    return render(request, 'labstatus/main.html', {"labs": labs})
