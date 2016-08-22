import datetime

from django.template import loader
from django.shortcuts import render

from mad_web.events.models import Event


# Create your views here.
def home_feed(request):
    now = datetime.datetime.now()
    now = now.replace(hour=0, minute=0, second=0, microsecond=0)
    event_list = Event.objects.order_by('start_time').filter(start_time__gte=now)

    data = {
        'event_list': event_list,
    }

    return render(request, 'home/home_feed.html', context=data)
