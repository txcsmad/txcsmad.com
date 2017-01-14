from os import path

from django import forms
from django.template.defaultfilters import filesizeformat


class MADconApplicationForm(forms.Form):
    T_SHIRT_SIZES = (("XS", "XS"),
                     ("S", "S"),
                     ("M", "M"),
                     ("L", "L"),
                     ("XL", "XL"))
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
    dietary_restrictions = forms.CharField(max_length=256)
    first_time = forms.BooleanField()
    t_shirt_size = forms.ChoiceField(choices=T_SHIRT_SIZES)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    concentration = forms.ChoiceField(choices=CONCENTRATION_CHOICES)
    resume = forms.FileInput(attrs={'placeholder': 'Resume file'})
    graduation_date = forms.DateInput()

    ONE_MB = 1048576
    PDF_TYPE = '.pdf'

    def register_for_madcon(self):
        pass

    def clean(self):
        cleaned_data = super(MADconApplicationForm, self).clean()
        resumeFile = cleaned_data['resume']

        if resumeFile:
            # If file is not PDF, then don't allow
            fileName, fileExt = path.splitext(resumeFile.name)
            if fileExt != self.PDF_TYPE:
                raise forms.ValidationError('Please put in a pdf file for your resume')
            # If file is over 1MB, then don't allow
            if resumeFile.size > self.ONE_MB:
                raise forms.ValidationError('Please use a file smaller than %s. Current filesize %s') % (
                    filesizeformat(self.ONE_MB), filesizeformat(resumeFile.size))

                return cleaned_data

class MADconConfirmAttendanceForm(forms.Form):
    def confirm_attendance(self):
        pass
