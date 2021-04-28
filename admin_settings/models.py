from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class How_it_works(models.Model):

	title=models.CharField(max_length= 20, blank=True, null=True)
	image = models.ImageField(upload_to='how_it_work_images', null=True,blank=True)
	line_image = models.ImageField(upload_to='how_it_work_images', null=True,blank=True)
	description = models.CharField(max_length= 200, blank=True, null=True)
	created_date = models.DateTimeField(default=timezone.now)
	created_by = models.ForeignKey(User,related_name='how_it_work_created_by', on_delete=models.CASCADE)

	def __str__(self):
		return str(self.title)


class System_settings(models.Model):
   
	logo = models.ImageField(upload_to='logo_images', null=True,blank=True)
	footer_logo=models.ImageField(upload_to='logo_images',null=True, blank=True)
	header_bg_img = models.ImageField(upload_to='header_bg_img_images', blank=True, null=True)
	find_supplier_bg_img = models.ImageField(upload_to='header_bg_img_images', blank=True, null=True)
	find_services_bg_img = models.ImageField(upload_to='header_bg_img_images', blank=True, null=True)
	find_products_bg_img = models.ImageField(upload_to='header_bg_img_images', blank=True, null=True)
	supplier_dashboard_bg_img = models.ImageField(upload_to='header_bg_img_images', blank=True, null=True)
	customer_dashbaord_bg_img = models.ImageField(upload_to='header_bg_img_images', blank=True, null=True)
	about_us_bg_img = models.ImageField(upload_to='header_bg_img_images', blank=True, null=True)
	service_counter = models.IntegerField(blank=True, null=True)

	product_counter = models.IntegerField(blank=True, null=True)
	supplier_counter = models.IntegerField(blank=True, null=True)
	header_service_icon=models.ImageField(upload_to='icon_images', null=True,blank=True)
	header_supplier_icon=models.ImageField(upload_to='icon_images', null=True,blank=True)
	service_icon=models.ImageField(upload_to='icon_images', null=True,blank=True)
	supplier_icon=models.ImageField(upload_to='icon_images', null=True,blank=True)
	product_icon=models.ImageField(upload_to='icon_images', null=True,blank=True)
	about_image=models.ImageField(upload_to='about_images', blank=True, null=True)
	about_title=models.CharField(max_length= 20, blank=True, null=True)
	about_description = models.CharField(max_length= 300, blank=True, null=True)
	fb = models.URLField(max_length = 200,blank=True, null=True) 
	twitter = models.URLField(max_length = 200,blank=True, null=True) 
	linkedin = models.URLField(max_length = 200,blank=True, null=True)
	created_date = models.DateTimeField(default=timezone.now)
	created_by = models.ForeignKey(User,related_name='system_settings_created_by', on_delete=models.CASCADE)
	def __str__(self):
		return str(self.created_by)