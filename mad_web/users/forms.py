from django import forms
from django.contrib.auth import get_user_model
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from os import path

from .models import User


class UserSignupForm(forms.ModelForm):
    ONE_MB = 1048576
    PDF_TYPE = '.pdf'

    class Meta:

        model = User
        fields = ['full_name', 'nick_name', 'graduation_date', 'resume']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'nick_name': forms.TextInput(attrs={'placeholder': 'Nick Name'}),
            'graduation_date': forms.TextInput(attrs={'placeholder': 'Graduation Date'}),
            'resume': forms.FileInput(attrs={'placeholder': 'Resume file'}),
        }

    # Clean the resume file to make sure it is .pdf and is under 1MB
    def clean(self):
        cleaned_data = super(UserSignupForm, self).clean()
        resumeFile = cleaned_data['resume']

        if resumeFile:
            # If file is not PDF, then don't allow
            fileName, fileExt = path.splitext(resumeFile.name)
            if fileExt != self.PDF_TYPE:
                raise forms.ValidationError(_('Please put in a pdf file for your resume'))
            # If file is over 1MB, then don't allow
            if resumeFile.size > self.ONE_MB:
                raise forms.ValidationError(_('Please keep resume filesize under %s. Current filesize %s') % (
                filesizeformat(self.ONE_MB), filesizeformat(resumeFile.size)))

        return cleaned_data

    def signup(self, request, user):
        user.username = self.cleaned_data['username']
        user.full_name = self.cleaned_data['full_name']
        user.nick_name = self.cleaned_data['nick_name']
        user.graduation_date = self.cleaned_data['graduation_date']
        user.resume = self.cleaned_data['resume']
        user.save()
