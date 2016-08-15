# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the GoSetupView
    url(
        regex=r'^$',
        view=views.EventListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^(?P<id>[\w.@+-]+)/$',
        view=views.EventDetailView.as_view(),
        name='detail'
    ),
]
