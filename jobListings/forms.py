from django import forms
from .models import JobListing, JobApplication

class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        # fields = ['role', 'location', 'industry', 'description', 'salary', 'vacancies']
        fields = ['role', 'location', 'description', 'salary', 'vacancies']