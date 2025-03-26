from django.db import models
from users.models import CustomUser as User

# Create your models here.

class Resume(models.Model):
    resume = models.FileField(upload_to='resume/files')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.email
