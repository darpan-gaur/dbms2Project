from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import JobListing, JobApplication
from .forms import JobListingForm
from users.models import CustomUser as User
from recruiter.models import RecruitingCompany as R
from django.contrib import messages

# Create your views here.
# @TODO: Add a view to display all job listings
# @TODO: Add a view to display only job listings posted by the logged in user
# @TODO: Add a view to add a job listing
# @TODO: Add a view to update a job listing
# @TODO: Add a view to delete a job listing
# @TODO: Add a view to view a job listing
# @TODO: Add a view to apply for a job
# @TODO: Add a view to view all job applications for the logged in user
# @TODO: Add a view to view all job applications for a job listing posted by the logged in user


def view_all_job_listings(request):
    job_listings = JobListing.objects.all() # write a raw query
    return render(request, 'jobListings/job_listings.html', {'job_listings': job_listings})

def add_job_listing(request):
    if request.user.is_authenticated and request.user.is_recruiter:
        if request.method == 'POST':
            form = JobListingForm(request.POST)
            if form.is_valid():
                job_listing = form.save(commit=False)
                job_listing.posted_by = request.user
                company:R = R.objects.filter(user=request.user)
                if company.exists():
                    job_listing.company = company.first()
                else:
                    messages.error(request, 'You need to create a company profile to post a job listing')
                    return redirect('recruiter_profile')
                job_listing.save()
                return redirect('your_job_listings')
        else:
            form = JobListingForm()
        return render(request, 'jobListings/add_job.html', {'form': form})
    else:
        messages.error(request, 'You need to be logged in as a recruiter to post a job listing')
        return redirect('login')
    
def update_job_listing(request, job_id):
    job_listing = JobListing.objects.get(id=job_id)
    if request.is_authenticated and request.user == job_listing.posted_by and request.user.is_company:
        if request.method == 'POST':
            form = JobListingForm(request.POST, instance=job_listing)
            if form.is_valid():
                job_listing = form.save(commit=False)
                job_listing.posted_by = request.user
                company:R = R.objects.filter(user=request.user)
                if company.exists():
                    job_listing.company = company.first()
                else:
                    messages.error(request, 'You need to create a company profile to post a job listing')
                    return redirect('recruiter_profile')
                job_listing.save()
                return redirect('your_job_listings')
        else:
            form = JobListingForm(instance=job_listing)
        return render(request, 'jobListings/update_job_listing.html', {'form': form})
    else:
        messages.error(request, 'You are not authorized to update this job listing')
        return redirect('job_listings')
    
def delete_job_listing(request, job_id):
    job_listing = JobListing.objects.filter(id=job_id)
    if not job_listing.exists():
        messages.error(request, 'Job listing not found')
        return redirect('job_listings')
    
    job_listing = job_listing.first()
    if request.user == job_listing.posted_by:
        job_listing.delete()
        return redirect('your_job_listings')
    else:
        messages.error(request, 'You are not authorized to delete this job listing')
        return redirect('job_listings')
    
def view_job_listing(request, job_id):
    job_listing = JobListing.objects.get(id=job_id)
    return render(request, 'jobListings/view_job_listing.html', {'job_listing': job_listing})

def apply_for_job(request, job_id):
    if request.user.is_authenticated and not request.is_applicant:
        job_listing = JobListing.objects.get(id=job_id)
        if JobApplication.objects.filter(user=request.user, job=job_listing).exists():
            messages.error(request, 'You have already applied for this job')
            return redirect('job_listings')
        else:
            job_application = JobApplication(user=request.user, job=job_listing)
            job_application.save()
            messages.success(request, 'You have successfully applied for this job')
            return redirect('job_listings')
    else:
        messages.error(request, 'You need to be logged in as a job seeker to apply for a job')
        return redirect('login')
    
def your_job_listings(request):
    if request.user.is_authenticated and request.user.is_company:
        job_listings = JobListing.objects.filter(posted_by=request.user)
        return render(request, 'jobListings/job_listings.html', {'job_listings': job_listings})
    else:
        messages.error(request, 'You need to be logged in as a recruiter to view your job listings')
        return redirect('login')
    
def your_job_applications(request):
    if request.user.is_authenticated and request.user.is_applicant:
        job_applications = JobApplication.objects.filter(user=request.user)
        return render(request, 'jobListings/your_job_applications.html', {'job_applications': job_applications})
    else:
        messages.error(request, 'You need to be logged in as a job seeker to view your job applications')
        return redirect('login')
