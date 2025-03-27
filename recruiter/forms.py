from django import forms
from .models import RecruitingCompany

# TODO: add industry to the feilds

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruitingCompany
        fields = ['company_name', 'company_description']
