from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Go(models.Model):
    id = models.CharField(
        _('ID for Go'),
        primary_key=True,
        unique=True,
        max_length=255,
        help_text=_('Required. 255 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[a-zA-Z0-9_-]+$',
                _('Enter a valid Go ID. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _("A Go Link with that ID already exists."),
        },
    )
    url = models.CharField(
        _('URL'),
        max_length=255,
        help_text=_('Required. 255 characters or fewer.'),
        validators=[
            validators.RegexValidator(
                r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
                _('Enter a valid Go URL.')
            ),
        ],
    )
