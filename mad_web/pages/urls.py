# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^workshops/$', TemplateView.as_view(template_name='pages/workshops.html'), name='workshops'),
    # url(r'^labs/$', TemplateView.as_view(template_name='pages/labs.html'), {
    #     'description': 'MAD Labs is a subset of the most technically experienced and passionate MAD members that focuses on creating quality mobile apps for others. Members specialize in iOS, Android, Windows or web platforms.'},
    #     name='labs'),
]
