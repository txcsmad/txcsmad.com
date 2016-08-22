import datetime

from django.template import loader
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.utils.safestring import mark_safe

from .models import Event, EventCalendar


class EventListView(ListView):
    model = Event
    # These next two lines tell the view to index lookups by username
    slug_field = 'startTime'
    slug_url_kwarg = 'startTime'

    def get_queryset(self):
        qs = super(EventListView, self).get_queryset()
        now = datetime.datetime.now()
        now = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return qs.filter(start_time__gte=now)


def calendar(request, year=datetime.datetime.now().year, month=datetime.datetime.now().month):
    template = loader.get_template('events/event_calendar.html')

    # setup arguments, as it is a string and needs to be an int
    year = int(year)
    month = int(month)

    event_list = Event.objects.order_by('start_time').filter(
        start_time__year=year, start_time__month=month
    )
    calendar_html = EventCalendar(event_list).formatmonth(year, month)

    data = {
        'calendar': mark_safe(calendar_html)
    }
    return render(request, 'events/event_calendar.html', context=data)


class EventDetailView(DetailView):
    model = Event
    slug_field = 'id'
    slug_url_kwarg = 'id'
