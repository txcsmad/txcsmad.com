# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from mad_web.labstatus import views

urlpatterns = [
    # URL pattern for the app
    url(
        regex=r'^$',
        view=views.main_app,
        name='main'
    ),
    url(
        regex=r'^backend-proxy$',
        view=views.backend_proxy,
        name='labs-proxy'
    ),

]
