# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import hashlib

from django.contrib.auth.models import Group, AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    full_name = models.CharField(_('Full Name'), max_length=255)
    nick_name = models.CharField(_('Nick Name'), max_length=255)
    graduation_date = models.DateField(_('Graduation Date'))

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
        return self.is_active and not self.is_staff and not self.groups.filter(name="Sponsor").exists()

    def is_officer(self):
        return self.is_staff

    def is_sponsor(self):
        return self.groups.filter(name="Sponsor").exists()


class UserService():
    # User Getters

    @staticmethod
    def get_inactive_users(self):
        user_list = User.objects.all()
        inactive_list = []
        for user in user_list:
            if user.is_disabled():
                inactive_list.append(user)
        return inactive_list

    @staticmethod
    def get_active_users(self):
        user_list = User.objects.all()
        active_list = []
        for user in user_list:
            if user.is_member():
                active_list.append(user)
        return active_list

    @staticmethod
    def get_officer_users(self):
        user_list = User.objects.all()
        staff_list = []
        for user in user_list:
            if user.is_officer():
                staff_list.append(user)
        return staff_list

    @staticmethod
    def get_sponsor_users(self):
        return Group.objects.get("Sponsor").user_set

    # Email Getters

    @staticmethod
    def get_inactive_users_emails(self):
        user_list = User.objects.all()
        inactive_email_list = []
        for user in user_list:
            if user.is_disabled():
                inactive_email_list.append(user.email)
        return inactive_email_list

    @staticmethod
    def get_active_users_emails(self):
        user_list = User.objects.all()
        active_email_list = []
        for user in user_list:
            if user.is_member():
                active_email_list.append(user.email)
        return active_email_list

    @staticmethod
    def get_officer_users_emails(self):
        user_list = User.objects.all()
        officer_email_list = []
        for user in user_list:
            if user.is_officer():
                officer_email_list.append(user.email)
        return officer_email_list

    @staticmethod
    def get_sponsor_users_emails(self):
        user_list = Group.objects.get("Sponsor").user_set
        sponsor_email_list = []
        for user in user_list:
            sponsor_email_list.append(user.email)
        return sponsor_email_list
