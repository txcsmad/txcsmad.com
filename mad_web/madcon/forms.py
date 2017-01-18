import datetime
from os import path

from django import forms
from django.template.defaultfilters import filesizeformat

from mad_web.madcon.models import Registration, MADcon
from mad_web.users.models import GENDER_CHOICES, CONCENTRATION_CHOICES


class MADconApplicationForm(forms.Form):
    t_shirt_size = forms.ChoiceField(choices=Registration.T_SHIRT_SIZES)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    concentration = forms.ChoiceField(choices=CONCENTRATION_CHOICES)
    graduation_date = forms.DateField()
    resume = forms.FileField()

    dietary_restrictions = forms.CharField(max_length=256, required=False)
    first_time = forms.BooleanField(required=False)
    ONE_MB = 1048576
    PDF_TYPE = '.pdf'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MADconApplicationForm, self).__init__(*args, **kwargs)

    def register_for_madcon(self):
        user = self.request.user
        user.resume = self.cleaned_data["resume"]
        user.graduation_date = self.cleaned_data["graduation_date"]
        user.concentration = self.cleaned_data["concentration"]
        user.gender = self.cleaned_data["gender"]

        most_recent_madcon = MADcon.objects.get(date__year=datetime.datetime.now().year)
        registration = Registration()
        registration.user = self.request.user
        registration.madcon = most_recent_madcon
        registration.first_time = self.cleaned_data["first_time"]
        registration.dietary_restrictions = self.cleaned_data["dietary_restrictions"]
        registration.t_shirt_size = self.cleaned_data["t_shirt_size"]
        registration.status = "P"

        registration.save()

    def clean(self):
        cleaned_data = super(MADconApplicationForm, self).clean()
        resume_file = cleaned_data['resume']

        if resume_file:
            # If file is not PDF, then don't allow
            file_name, file_ext = path.splitext(resume_file.name)
            if file_ext != self.PDF_TYPE:
                raise forms.ValidationError('Please attach a resume')
            # If file is over 1MB, then don't allow
            if resume_file.size > self.ONE_MB:
                raise forms.ValidationError('Please use a file smaller than %s. Current filesize %s') % (
                    filesizeformat(self.ONE_MB), filesizeformat(resume_file.size))

        user = self.request.user
        existing_application = Registration.objects.filter(user=user)
        if len(existing_application) > 0:
            raise forms.ValidationError("You've already registered for MADcon")
        return cleaned_data

class MADconConfirmAttendanceForm(forms.Form):
    def confirm_attendance(self):
        pass
