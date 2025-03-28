from django.shortcuts import render
from jobListings.models import JobListing, JobType
from locations.models import Locations
from industries.models import Industries
from .filter import Jobfilter

# Create your views here.
def home_view(request):

    query_params = {
        'company_name': request.GET.get('company_name'),
        'location': request.GET.get('location'),
        'industry': request.GET.get('industry'),
        'job_type': request.GET.get('job_type'),
        'title': request.GET.get('title'),
    }

    raw_query = 'SELECT * FROM "jobListings_joblisting" WHERE 1=1'  # Use lowercase table name
    params = []

    if query_params.get('company_name'):
        raw_query += " AND company_id IN (SELECT id FROM recruiter_recruitingcompany WHERE company_name ILIKE %s)"
        params.append(f"%{query_params['company_name']}%")

    if query_params.get('location'):
        raw_query += " AND location_id = %s"
        params.append(int(query_params['location']))

    if query_params.get('industry'):
        raw_query += " AND industry_id = %s"
        params.append(int(query_params['industry']))

    if query_params.get('job_type'):
        raw_query += " AND job_type_id = %s"
        params.append(int(query_params['job_type']))

    if query_params.get('title'):
        raw_query += " AND role ILIKE %s"
        params.append(f"%{query_params['title']}%")

    raw_query += ';'
    print("Generated SQL:", raw_query)  # Debugging

    job_listings = JobListing.objects.raw(raw_query, params)

    return render(request, 'homepage/home.html', {'job_filters': job_listings, 'locations': Locations.objects.all(), 'industries': Industries.objects.all(), 'job_types': JobType.objects.all()})


    
    
    
    

        
