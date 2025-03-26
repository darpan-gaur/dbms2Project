from django import forms
from .models import Skills, Applicant

class ApplicantProfileForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['location', 'skills', 'phone_number']
        widgets = {
            'skills': forms.CheckboxSelectMultiple(),
        }

        
