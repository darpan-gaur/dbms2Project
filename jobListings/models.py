from django.db import models
from users.models import CustomUser as User
from resume.models import Resume
from recruiter.models import RecruitingCompany as R
from locations.models import Locations
from industries.models import Industries
from applicant.models import Applicant

# Create your models here.

class JobType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class JobListing(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(R, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE, null=True)
    industry = models.ForeignKey(Industries, on_delete=models.CASCADE, null=True)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE, default=1)
    description = models.TextField()
    salary = models.IntegerField()
    vacancies = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role + ' - ' + self.company.company_name

class JobStatus(models.Model):
    status = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.status

class JobApplication(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(JobStatus, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.applicant.user.email + ' - ' + self.job.role
    

