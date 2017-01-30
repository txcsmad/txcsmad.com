from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from mad_web.madcon.models import Registration
from mad_web.users.models import User


class MADconRegisterationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['t_shirt_size', 'first_time', 'dietary_restrictions']


class UserResumeForm(forms.ModelForm):
    resume = forms.FileField(widget=AdminFileWidget, required=False)

    class Meta:
        model = User
        fields = ['gender', 'concentration', 'graduation_date', 'resume']


UserResumeInlineFormSet = forms.inlineformset_factory(User, Registration,
                                                      form=MADconRegisterationForm, extra=1,
                                                      can_delete=False)


class MADconConfirmAttendanceForm(forms.Form):
    def confirm_attendance(self):
        print(self.data)
        registration_id = int(self.data['registration_id'])

        registration = get_object_or_404(Registration, pk=registration_id)
        if registration.status != "A":
            raise ValidationError(_('Invalid registration status'), code='invalid_status')
        registration.status = "C"
        registration.save()
        pass
