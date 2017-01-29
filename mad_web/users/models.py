# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import hashlib

from django.contrib.auth.models import Group, AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from .validators import validate_file_extension
from .validators import validate_file_size

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
    ("N", "Non - binary"),
    ("P", "Prefer not to answer"))
CONCENTRATION_CHOICES = (
    ("CS", "Computer Science"),
    ("D", "Design"),
    ("B", "Business"),
    ("EE", "Electrical Engineering"),
    ("M", "Math"),
    ("O", "Other")
)

@python_2_unicode_compatible
class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255)
    graduation_date = models.DateField()     
    resume = models.FileField(upload_to='resumes/', blank=True, null=True, validators=[validate_file_extension, validate_file_size])
    concentration = models.CharField(max_length=3, choices=CONCENTRATION_CHOICES, blank=True, default="CS", null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, default="M", null=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_gravatar_image_url(self):
        return 'https://secure.gravatar.com/avatar/' + hashlib.md5(
            self.email.lower().encode('utf-8')).hexdigest() + '?s=300'

    # User Type

    def is_disabled(self):
        return not self.is_active

    def is_member(self):
        return self.is_active and not self.is_officer() and not self.is_ta() and not self.is_sponsor()

    def is_officer(self):
        return self.groups.filter(name="Officer").exists() and self.is_staff

    def is_ta(self):
        return self.groups.filter(name="TA").exists()

    def is_sponsor(self):
        return self.groups.filter(name="Sponsor").exists()


class UserService:
    # User Getters

    @staticmethod
    def get_inactive_users():
        user_list = User.objects.all()
        inactive_list = []
        for user in user_list:
            if user.is_disabled():
                inactive_list.append(user)
        return inactive_list

    @staticmethod
    def get_active_users():
        user_list = User.objects.all()
        active_list = []
        for user in user_list:
            if user.is_member():
                active_list.append(user)
        return active_list

    @staticmethod
    def get_officer_users():
        user_list = User.objects.all()
        staff_list = []
        for user in user_list:
            if user.is_officer():
                staff_list.append(user)
        return staff_list

    @staticmethod
    def get_sponsor_users():
        return Group.objects.get("Sponsor").user_set

    # Email Getters

    @staticmethod
    def get_inactive_users_emails():
        user_list = User.objects.all()
        inactive_email_list = []
        for user in user_list:
            if user.is_disabled():
                inactive_email_list.append(user.email)
        return inactive_email_list

    @staticmethod
    def get_active_users_emails():
        user_list = User.objects.all()
        active_email_list = []
        for user in user_list:
            if user.is_member():
                active_email_list.append(user.email)
        return active_email_list

    @staticmethod
    def get_officer_users_emails():
        user_list = User.objects.all()
        officer_email_list = []
        for user in user_list:
            if user.is_officer():
                officer_email_list.append(user.email)
        return officer_email_list

    @staticmethod
    def get_sponsor_users_emails():
        user_list = Group.objects.get("Sponsor").user_set
        sponsor_email_list = []
        for user in user_list:
            sponsor_email_list.append(user.email)
        return sponsor_email_list
    
    @staticmethod
    def get_madcon_pending_emails():
        from mad_web.madcon.models import Registration
        registrations = Registration.objects.filter(status="P").prefetch_related("user")
        pending_email_list = []
        for registration in registrations:
            pending_email_list.append(registration.user.email)
        return pending_email_list


    @staticmethod
    def get_madcon_accepted_emails():
        from mad_web.madcon.models import Registration
        registrations = Registration.objects.filter(status="A").prefetch_related("user")
        accepted_email_list = []
        for registration in registrations:
            accepted_email_list.append(registration.user.email)
        return accepted_email_list

    @staticmethod
    def get_madcon_confirmed_emails():
        from mad_web.madcon.models import Registration
        registrations = Registration.objects.filter(status="C").prefetch_related("user")
        confirmed_email_list = []
        for registration in registrations:
            confirmed_email_list.append(registration.user.email)
        return confirmed_email_list