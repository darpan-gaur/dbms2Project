from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_job_listings, name='view_job_listings'),
    path('add/', views.add_job, name='add_job'),
]