from django import forms
from .models import Skills, Applicant
from resume.models import Resume

class ApplicantProfileForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skills.objects.all(), 
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    
    class Meta:
        model = Applicant
        fields = ['location', 'skills', 'phone_number']

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['resume']
