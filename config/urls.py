# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework import routers

from mad_web import pages
from mad_web.events.views import EventViewSet, MadConScheduleViewSet
from mad_web.madcon.views import MyRegistrationViewSet, MADconViewSet, RegistrationViewSet
from mad_web.users.views import UserViewSet, MeView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'events', EventViewSet)
router.register(r'madcon_schedule', MadConScheduleViewSet)
router.register(r'madcon/myregistration', MyRegistrationViewSet)
router.register(r'madcon/registration', RegistrationViewSet)
router.register(r'madcon', MADconViewSet)

urlpatterns = [
                  url(r'^', include('mad_web.pages.urls')),
                  # Django Admin, use {% url 'admin:index' %}
                  url(settings.ADMIN_URL, include(admin.site.urls)),

                  # Lab Status
                  url(r'^labstatus/', include("mad_web.labstatus.urls")),

                  # User management
                  url(r'^users/', include('mad_web.users.urls', namespace='users')),
                  url(r'^accounts/', include('allauth.urls')),

                  # API Rest Framework
                  url(r'^api/v1/me/', MeView.as_view()),
                  url(r'^api/v1/', include(router.urls)),
                  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

                  # Your stuff: custom urls includes go here
                  url(r'^events/', include('mad_web.events.urls', namespace='events')),
                  url(r'^madcon/', include('mad_web.madcon.urls', namespace='madcon')),
                  url(r'^', include('mad_web.home.urls', namespace='home')),
                  url(r'^go/', include('mad_web.go.urls', namespace='go')),
                  url(r'^notify/', include('mad_web.notify.urls', namespace='notify')),

                  # OAuth
                  url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider'))

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
