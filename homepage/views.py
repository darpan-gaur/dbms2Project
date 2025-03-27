from django.shortcuts import render
from jobListings.models import JobListing, JobApplication
from .filter import Jobfilter

# Create your views here.
def home_view(request):
    job_listings = JobListing.objects.all()
    job_filter = Jobfilter(request.GET, queryset=job_listings)
    # job_listings = job_filter.qs
    context = {
        'filter': job_filter,
    }
    return render(request, 'homepage/home.html', context)

    
    
    
    

        
