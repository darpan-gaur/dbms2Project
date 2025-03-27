from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_all_job_listings, name='view_all_job_listings'),
    path('add/', views.add_job_listing, name='add_job'),
    path('update/<int:job_id>/', views.update_job_listing, name='update_job'),
    path('delete/<int:job_id>/', views.delete_job_listing, name='delete_job'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_job'),
    path('your-job-listings/', views.your_job_listings, name='your_job_listings'),
    path('your-job-applications/', views.your_job_applications, name='your_job_applications'),
]