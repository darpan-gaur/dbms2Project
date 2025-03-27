from django.urls import path
from . import views

urlpatterns = [
    path("update-recruiter/", views.update_recruiter_profile, name="update_recruiter"),
    path("recruiter-profile/", views.view_recruiter_profile, name="recruiter_profile"),
]