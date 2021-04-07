from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, auth
from autoslug import AutoSlugField
# Create your models here.
class AboutUs(models.Model):
	image = models.ImageField(upload_to='about_us_images', blank=True)
	description = models.TextField(blank=True, null=True)
	created_date = models.DateTimeField(default=timezone.now)
	created_by = models.ForeignKey(User,related_name='aboutuscreated_by', on_delete=models.CASCADE)


	def __str__(self):
		return str(self.created_by)

class CustomPage(models.Model):
	page_name=models.CharField(max_length=30, null=True, blank=True)
	header_image = models.ImageField(upload_to='header_images', blank=True)
	description = models.TextField(blank=True, null=True)
	slug= AutoSlugField(populate_from='page_name', null=True, blank=True)
	created_date = models.DateTimeField(default=timezone.now)
	created_by = models.ForeignKey(User,related_name='custom_page_created_by', on_delete=models.CASCADE)


	def __str__(self):
		return str(self.page_name)