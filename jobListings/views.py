from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import JobListing, JobApplication, JobType, JobStatus
from .forms import JobListingForm
from users.models import CustomUser as User
from recruiter.models import RecruitingCompany as R
from django.contrib import messages
from applicant.models import Applicant
from notifications.models import Notification
from industries.models import Industries
from locations.models import Locations


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
    return render(request, 'jobListings/all_job_listings.html', {'jobs': JobListing.objects.all()})

def add_job_listing(request):
    if request.user.is_authenticated and request.user.is_company:
        if request.method == 'POST':
            form = JobListingForm(request.POST)
            if form.is_valid():
                job_listing = form.save(commit=False)
                job_listing.posted_by = request.user
                company:R = R.objects.filter(user=request.user)
                applicants = Applicant.objects.all()
                
                if company.exists():
                    for applicant in applicants:
                        notification = Notification(user=applicant.user, message=f'{request.user.first_name} has posted a new job listing for the role {job_listing.role} at {company.first().company_name}')
                        notification.save()
                    job_listing.company = company.first()
                    messages.success(request, 'Job listing added successfully')
                else:
                    messages.error(request, 'You need to create a company profile to post a job listing')
                    return redirect('recruiter_profile')
                job_listing.save()
                return redirect('your_job_listings')
        else:
            form = JobListingForm()
        return render(request, 'jobListings/add_job.html', {'form': form, 'locations': Locations.objects.all(), 'industries': Industries.objects.all(), 'job_types': JobType.objects.all()})
    else:
        messages.error(request, 'You need to be logged in as a recruiter to post a job listing')
        return redirect('login')
    
def update_job_listing(request, job_id):
    job_listing = JobListing.objects.get(id=job_id)
    print("hellO",job_listing.role)
    if request.user.is_authenticated and request.user == job_listing.posted_by and request.user.is_company:
        if request.method == 'POST':
            form = JobListingForm(request.POST, instance=job_listing)
            if form.is_valid():
                job_listing = form.save(commit=False)
                job_listing.posted_by = request.user
                company:R = R.objects.filter(user=request.user)
                applicants = Applicant.objects.all()
                if company.exists():
                    job_listing.company = company.first()
                    for applicant in applicants:
                        notification = Notification(user=applicant.user, message=f'{request.user.first_name} has updated a job listing')
                        notification.save()
                else:
                    messages.error(request, 'You need to create a company profile to post a job listing')
                    return redirect('recruiter_profile')
                job_listing.save()
                return redirect('your_job_listings')
        else:
            form = JobListingForm(instance=job_listing)
        return render(request, 'jobListings/update_job_listing.html', {'form': form, 'locations': Locations.objects.all(), 'industries': Industries.objects.all(), 'job_types': JobType.objects.all()})
    else:
        messages.error(request, 'You are not authorized to update this job listing')
        return redirect('home')
    
def delete_job_listing(request, job_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be logged in to delete a job listing')
        return redirect('login')
    if not request.user.is_company:
        messages.error(request, 'You need to be logged in as a recruiter to delete a job listing')
        return redirect('home')

    job_listing = JobListing.objects.filter(id=job_id)
    if not job_listing.exists():
        messages.error(request, 'Job listing not found')
        return redirect('job_listings')
    
    job_listing = job_listing.first()
    if request.user == job_listing.posted_by:
        applicants = JobApplication.objects.filter(job=job_listing)
        for applicant in applicants:
            Notification.objects.filter(user=applicant.user, message=f'{request.user.first_name} has deleted a job listing')
        job_listing.delete()
        return redirect('your_job_listings')
    else:
        messages.error(request, 'You are not authorized to delete this job listing')
        return redirect('job_listings')
    
def view_job_listing(request, job_id):
    job_listing = JobListing.objects.get(id=job_id)
    return render(request, 'jobListings/job_details.html', {'job': job_listing})

def apply_for_job(request, job_id):
    # print("here", request.user.is_authenticated, request.user.is_applicant, request.user.is_company)
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be logged in to apply for a job')
        return redirect('login')
    elif request.user.is_company:
        messages.error(request, 'You need to be logged in as an applicant to apply for a job')
        return redirect('home')
    elif request.user.is_applicant:
        job_listing = JobListing.objects.get(id=job_id)
        # print(request.user.is_applicant)
        applicant = Applicant.objects.filter(user=request.user)
        if not applicant.exists():
            messages.error(request, 'You need to create an applicant profile to apply for a job')
            return redirect('update_applicant')
        applicant = applicant.first()
        # check if the applicant has already applied for the job
        job_application = JobApplication.objects.filter(applicant=applicant.first(), job=job_listing)
        if job_application.exists():
            messages.error(request, 'You have already applied for this job')
            return redirect('home')
        if not applicant.exists():
            messages.error(request, 'You need to create an applicant profile to apply for a job')
            return redirect('applicant_profile')
        applicant = applicant.first()
        
        job_application = JobApplication(applicant=applicant, job=job_listing, status=JobStatus.objects.get(id=1))
        applicant_name = f'{applicant.user.first_name} {applicant.user.last_name}'
        Notification.objects.create(user=job_listing.posted_by, message=f'{applicant_name} has applied for the job {job_listing.role}')
        job_application.save()
        return redirect('applied_jobs')
    
    
def your_job_listings(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be logged in as a recruiter to view your job listings')
        return redirect('login')
    elif request.user.is_applicant:
        messages.error(request, 'You need to be logged in as a recruiter to view your job listings')
        return redirect('home')
    elif request.user.is_company:
        job_listings = JobListing.objects.filter(posted_by=request.user)
        return render(request, 'jobListings/your_job_listings.html', {'jobs': job_listings})
    else:
        messages.error(request, 'You need to be logged in as a recruiter to view your job listings')
        return redirect('home')
    
def your_job_applications(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be logged in as an applicant to view your job applications')
        return redirect('login')
    elif request.user.is_company:
        messages.error(request, 'You need to be logged in as an applicant to view your job applications')
        return redirect('home')
    elif request.user.is_applicant:
        applicant = Applicant.objects.filter(user=request.user)
        if not applicant.exists():
            messages.error(request, 'You need to create an applicant profile to view your job applications')
            return redirect('update_applicant')
        applicant = applicant.first()
        job_applications = JobApplication.objects.filter(applicant=applicant)
        return render(request, 'jobListings/applied_jobs.html', {'job_applications': job_applications})
    else:
        messages.error(request, 'You need to be logged in as an applicant to view your job applications')
        return redirect('home')
    
def job_applications_for_job(request, job_id):
    job_listing = JobListing.objects.get(id=job_id)
    if request.user.is_authenticated and request.user.is_company and job_listing.posted_by == request.user:
        job_applications:JobApplication = JobApplication.objects.filter(job=job_listing)
        app_status = JobStatus.objects.all()
        return render(request, 'jobListings/job_applications.html', {'job_applications': job_applications, 'app_status': app_status})
    else:
        messages.error(request, 'You are not authorized to view job applications for this job listing')
        return redirect('home')
    

def withdraw_application(request, job_id):
    job_listing = JobListing.objects.get(id=job_id)
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be logged in as an applicant to withdraw an application')
        return redirect('login')
    elif request.user.is_company:
        messages.error(request, 'You need to be logged in as an applicant to withdraw an application')
        return redirect('home')
    elif request.user.is_applicant:
        applicant = Applicant.objects.filter(user=request.user)
        if not applicant.exists():
            messages.error(request, 'You need to create an applicant profile to withdraw an application')
            return redirect('update_applicant')
        applicant = applicant.first()
        job_application = JobApplication.objects.filter(applicant=applicant, job=job_listing)
        if job_application.exists():
            job_application.delete()
            messages.success(request, 'Application withdrawn successfully')
            return redirect('applied_jobs')
        else:
            messages.error(request, 'You have not applied for this job')
            return redirect('applied_jobs')
    else:
        messages.error(request, 'You need to be logged in as an applicant to withdraw an application')
        return redirect('home')
    
def update_application_status(request, app_id):
    print(app_id)
    job_application = JobApplication.objects.get(id=app_id)
    if request.user.is_authenticated and request.user.is_company and job_application.job.posted_by == request.user:
        if request.method == 'POST':
            status = request.POST.get('status')
            print(status)
            job_application.status = JobStatus.objects.get(id=status)
            job_application.save()
            messages.success(request, 'Application status updated successfully')
            return redirect('applications_for_job', job_id=job_application.job.id)
        else:
            messages.error(request, 'Invalid request')
            return redirect('applications_for_job', job_id=job_application.job.id)
    else:
        messages.error(request, 'You are not authorized to update the status of this application')
        return redirect('home')