from django.db import models
from users.models import CustomUser as User

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
    # resume = models.FileField(upload_to='resumes/') # onetomany relationship with resume model

    def __str__(self):
        return self.user.email