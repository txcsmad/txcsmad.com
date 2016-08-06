from django import forms
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from config.settings.common import EMAIL_WEBMASTER, DEFAULT_FROM_EMAIL
from mad_web.users.models import UserService


class NotifyForm(forms.Form):
    mailing_list = forms.ChoiceField(choices=(
        (0, _("Webmaster Test")),
        (1, _("Inactive")),
        (2, _("Members")),
        (3, _("Officers")),
        (4, _("Sponsors")),
    ))
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):

        email_to = []
        list_option = self.cleaned_data['mailing_list']
        if list_option == 1:
            email_to = UserService.get_inactive_users_emails()
        elif list_option == 2:
            email_to = UserService.get_active_users_emails()
        elif list_option == 3:
            email_to = UserService.get_officer_users_emails()
        elif list_option == 4:
            email_to = UserService.get_sponsor_users_emails()
        else:
            email_to = [EMAIL_WEBMASTER]

        send_mail(self.cleaned_data['subject'],
                  self.cleaned_data['message'],
                  DEFAULT_FROM_EMAIL,
                  email_to)
        pass
