from django.urls import path
from . import views

urlpatterns = [
    path("update-applicant/", views.update_applicant_view, name="update_applicant"),
    path("applicant-profile/", views.applicant_profile_view, name="applicant_profile"),
]