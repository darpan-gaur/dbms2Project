
from django.shortcuts import render
from .models import Locations

# Create your views here.
def view_locations(request):
    locations = Locations.objects.all()
    return render(request, 'locations/locations.html', {'locations': locations})