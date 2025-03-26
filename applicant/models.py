from django.db import models
from users.models import CustomUser as User
from resume.models import Resume

# Create your models here.
class Skills(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    
class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skills, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    # onetomany relationship with resume model
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True)
    #resume = models.FileField(upload_to='resumes/files', null=True, blank=True) 

    def __str__(self):
        return self.user.email
    
# class Resume(models.Model):
#     applicant = models.OneToOneField(Applicant, on_delete=models.CASCADE, related_name="resume")  
#     file = models.FileField(upload_to="resumes/")  
#     uploaded_at = models.DateTimeField(auto_now_add=True)