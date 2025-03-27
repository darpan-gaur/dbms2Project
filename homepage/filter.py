import django_filters
from jobListings.models import JobListing


class Jobfilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='role', lookup_expr='icontains')
    company_name = django_filters.CharFilter(field_name='company__name', lookup_expr='icontains')  # ✅ Add this filter
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')  # ✅ Add this filter

    class Meta:
        model = JobListing
        fields = ['role', 'company_name', 'location']
