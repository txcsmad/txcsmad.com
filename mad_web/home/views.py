import datetime

from django.template import loader, RequestContext
from django.shortcuts import HttpResponse

from mad_web.events.models import Event


# Create your views here.
def home_feed(request):
    template = loader.get_template('home/home_feed.html')

    now = datetime.datetime.now()
    event_list = Event.objects.order_by('start_time').filter(start_time__gte=now)

    context = RequestContext(request, {
        'event_list': event_list
    })
    return HttpResponse(template.render(context))
