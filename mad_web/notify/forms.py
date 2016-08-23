from django import forms
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _

from config.settings.common import EMAIL_WEBMASTER, DEFAULT_FROM_EMAIL
from mad_web.users.models import UserService
from mad_web.utils.utils import subscribe_to_newsletter


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
        list_option = int(self.cleaned_data['mailing_list'])
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

        mail = EmailMessage(subject=self.cleaned_data['subject'],
                            body=self.cleaned_data['message'],
                            from_email=DEFAULT_FROM_EMAIL)
        mail.bcc = email_to
        mail.to = [DEFAULT_FROM_EMAIL]
        mail.send()
        pass


class NotifyMeForm(forms.Form):
    email = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    def subscribe(self):
        subscribe_to_newsletter(self.cleaned_data['email'],
                                first_name=self.cleaned_data['first_name'],
                                last_name=self.cleaned_data['last_name'])
        pass
