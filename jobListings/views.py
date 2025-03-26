from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import JobListing, JobApplication
from .forms import JobListingForm
# Create your views here.

def view_job_listings(request):
    job_listings = JobListing.objects.all() # write a raw query
    return render(request, 'jobListings/job_listings.html', {'job_listings': job_listings})

def add_job(request):
    if request.method == 'POST':
        form = JobListingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_job_listings')
    else:
        form = JobListingForm()
    return render(request, 'jobListings/add_job.html', {'form': form})