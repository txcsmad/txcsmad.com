from django import forms


class MADconApplicationForm(forms.Form):
    dietary_restrictions = forms.CharField(max_length=256)
    first_time = forms.BooleanField()
    t_shirt_size = forms.CharField()


class MADconConfirmAttendanceForm(forms.Form):
    def confirm_attendance(self):
        pass
