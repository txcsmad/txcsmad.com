from django.contrib.auth import get_user_model
from django import forms

from .models import User

class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name','nick_name', 'graduation_date']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'nick_name': forms.TextInput(attrs={'placeholder': 'Nick Name'}),
            'graduation_date': forms.TextInput(attrs={'placeholder': 'Graduation Date'}),
        }

    def signup(self, request, user):
        user.username = self.cleaned_data['username']
        user.full_name = self.cleaned_data['full_name']
        user.nick_name = self.cleaned_data['nick_name']
        user.graduation_date = self.cleaned_data['graduation_date']
        user.save()
