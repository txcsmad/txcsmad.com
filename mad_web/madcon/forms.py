from django import forms
from django.contrib.admin.widgets import AdminFileWidget

from mad_web.madcon.models import Registration
from mad_web.users.models import User


class MADconRegisterationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['t_shirt_size', 'first_time','dietary_restrictions']
class UserResumeForm(forms.ModelForm):
    resume = forms.FileField(widget=AdminFileWidget, required=False)
    class Meta:
        model = User
        fields = ['gender', 'concentration', 'graduation_date', 'resume']
UserResumeInlineFormSet = forms.inlineformset_factory(User, Registration, form=MADconRegisterationForm, extra=1, can_delete=False)

class MADconConfirmAttendanceForm(forms.Form):
    def confirm_attendance(self):
        pass
