# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from mad_web.home.views import home_feed

urlpatterns = [
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^workshops/$', TemplateView.as_view(template_name='pages/workshops.html'), name='workshops'),
    url(r'^labs/$', TemplateView.as_view(template_name='pages/labs.html'), name='labs'),
    url(r'^gallery/$', TemplateView.as_view(template_name='pages/gallery.html'), name='gallery'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # User management
    url(r'^users/', include('mad_web.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here
    url(r'^events/', include('mad_web.events.urls', namespace='events')),
    url(r'^', include('mad_web.home.urls', namespace='home')),
    url(r'^go/', include('mad_web.go.urls', namespace='go')),
    url(r'^notify/', include('mad_web.notify.urls', namespace='notify'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
