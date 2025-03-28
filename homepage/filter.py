# import django_filters
# from jobListings.models import JobListing
# from locations.models import Locations
# from industries.models import Industries
# from jobListings.models import JobType


# class Jobfilter(django_filters.FilterSet):
#     title = django_filters.CharFilter(field_name='role', lookup_expr='icontains')
#     company_name = django_filters.CharFilter(field_name='company_name', lookup_expr='icontains')  # ✅ Add this filter
#     location = django_filters.ChoiceFilter(
#         field_name='location',
#         choices=[(location.id, location.name) for location in Locations.objects.all()],
#         empty_label='Select Location'
#     )
#     industry = django_filters.ChoiceFilter(
#         field_name='industry',
#         choices=[(industry.id, industry.name) for industry in Industries.objects.all()],
#         empty_label='Select Industry'
#     )
#     job_type = django_filters.ChoiceFilter(
#         field_name='job_type',
#         choices=[(job_type.id, job_type.name) for job_type in JobType.objects.all()],
#         empty_label='Select Job Type'
#     )

#     class Meta:
#         model = JobListing
#         fields = ['title', 'company_name', 'location', 'industry', 'job_type']
