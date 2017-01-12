from django.db import models

from mad_web.users.models import User


class MADcon(models.Model):
    date = models.DateField(unique_for_month=True)


class MADconApplication(models.Model):
    APPLICATION_STATUS_CHOICES = (
        ("P", "Pending"),
        ("A", "Accepted"),
        ("W", "Waitlisted"),
        ("R", "Rejected"),
        ("C", "Confirmed")
    )
    dietary_restrictions = models.CharField(blank=True, max_length=256)
    first_time = models.BooleanField()
    user = models.ForeignKey(User)
    status = models.CharField(choices=APPLICATION_STATUS_CHOICES, max_length=1)
    madcon = models.ForeignKey(MADcon)

    def __str__(self):
        return self.id
