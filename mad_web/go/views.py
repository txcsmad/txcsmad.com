from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Go

from mad_web.utils.utils import OfficerRequiredMixin


class GoSetupView(LoginRequiredMixin, ListView):
    model = Go
    slug_field = 'id'
    slug_url_kwarg = 'id'


def go(request, go_id):
    go = get_object_or_404(Go, pk=go_id)
    return HttpResponseRedirect(go.url)
