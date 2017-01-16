from django.db import models

from mad_web.users.models import User


class MADcon(models.Model):
    verbose_name = "MADcon"
    date = models.DateField(unique_for_month=True)


class Registration(models.Model):
    T_SHIRT_SIZES = (("XS", "XS"),
                     ("S", "S"),
                     ("M", "M"),
                     ("L", "L"),
                     ("XL", "XL"))
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
    t_shirt_size = models.CharField(choices=T_SHIRT_SIZES, max_length=3, blank=True)
    madcon = models.ForeignKey(MADcon)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
