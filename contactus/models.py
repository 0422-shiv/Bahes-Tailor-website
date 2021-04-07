from django.db import models
from django.utils import timezone

# Create your models here.
class ContactUs(models.Model):
    name = models.CharField(max_length=30,blank=True, null=True)
    email = models.EmailField(max_length=30,blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    reply_status=models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return str(self.name)
