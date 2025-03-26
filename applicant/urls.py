from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("update-applicant/", views.update_applicant_view, name="update_applicant"),
    path("applicant-profile/", views.applicant_profile_view, name="applicant_profile"),
    path("resume/", views.upload_resume, name="resume"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
