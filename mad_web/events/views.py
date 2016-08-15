from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Event


class EventListView(ListView):
    model = Event
    # These next two lines tell the view to index lookups by username
    slug_field = 'startTime'
    slug_url_kwarg = 'startTime'

class EventDetailView(DetailView):
    model = Event
    slug_field = 'id'
    slug_url_kwarg = 'id'
