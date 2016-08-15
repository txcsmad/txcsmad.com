from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _

EVENT_TAG = (
    (0, _("MAD")),
    (1, _("Android")),
    (2, _("iOS")),
    (3, _("Web")),
    (4, _("uMAD")),
    (5, _("Hack Night")),
    (6, _("Partner")),
)


class Event(models.Model):
    start_time = models.DateTimeField(_("Start Time"))
    end_time = models.DateTimeField(_("End Time"))
    title = models.CharField(_("Title"), max_length=255)
    location = models.CharField(_("Location"), max_length=255)
    description = models.TextField(_("Description"), null=True, blank=True)
    image_url = models.CharField(_("Image URL"), max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name=_("Creator"))
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    event_tags = ArrayField(models.IntegerField(_("Event Tag")), verbose_name=_("Event Tags"))
