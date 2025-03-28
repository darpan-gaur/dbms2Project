from django.shortcuts import render
from .models import Industries

# Create your views here.
def view_industries(request):
    industries = Industries.objects.all()
    return render(request, 'industries/industries.html', {'industries': industries})