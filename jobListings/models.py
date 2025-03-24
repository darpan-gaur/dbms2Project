from django.db import models
from User.models import User

# Create your models here.

class Industries(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Locations(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class JobType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Roles(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class JobListing(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #company
    # title = models.CharField(max_length=100)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    #role
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industries, on_delete=models.CASCADE)
    description = models.TextField()
    salary = models.IntegerField()
    vacancies = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #skills

    def __str__(self):
        return self.title

class JobStatus(models.Model):
    status = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.status

class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    # resume = models.FileField(upload_to='resumes/')
    # cover_letter = models.TextField()
    applied_on = models.DateTimeField(auto_now_add=True)

    status = models.ForeignKey(JobStatus, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' - ' + self.job.title
    

