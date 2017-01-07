# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    # URL pattern for the Events
    url(
        regex=r'^apply$',
        view=login_required(views.MADconApplicationView.as_view()),
        name='apply'
    ),
    url(
        regex=r'^(?P<id>[\w.@+-]+)/$',
        view=login_required(views.MADconApplicationStatusView.as_view()),
        name='status'
    ),
    url(
        regex=r'^confirm/(?P<id>[\w.@+-]+)/(?P<username>[\w.@+-]+)/$',
        view=login_required(views.MADconConfirmAttendanceView.as_view()),
        name='confirm'
    ),
]
