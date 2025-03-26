from django.db import models
from jobListings.models import Industries
from users.models import CustomUser as User

# Create your models here.

class RecruitingCompany(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    industry_id = models.ForeignKey(Industries, on_delete=models.CASCADE)
    # company_logo = models.ImageField(upload_to='company_logos/')
    company_description = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name
