from django.db import models

from mad_web.users.models import User


class MADcon(models.Model):
    date = models.DateField(unique_for_month="date")
    registration_open = models.BooleanField(default=False)
    class Meta:
        verbose_name = "MADcon"
        verbose_name_plural = "MADcons"
    


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
    user = models.OneToOneField(User)
    status = models.CharField(choices=APPLICATION_STATUS_CHOICES, max_length=1)
    t_shirt_size = models.CharField(choices=T_SHIRT_SIZES, max_length=3, blank=True, default="XS")
    madcon = models.ForeignKey(MADcon)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
