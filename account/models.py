from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from bahes.custom_lib import unique_otp_generator



class UserProfile(models.Model):
    user_id = models.OneToOneField(User,related_name='userx', on_delete=models.CASCADE)
    full_name=models.CharField(max_length= 50, blank=True, null=True)
    passward=models.CharField(max_length= 50, blank=True, null=True)

    image = models.ImageField(upload_to='images', blank=True)
    tel_code = models.IntegerField(blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True,unique=True)
    address = models.CharField(max_length= 100, blank=True, null=True)
    country = models.ForeignKey('Countries', on_delete=models.CASCADE)
    user_type = models.ForeignKey('UserType', on_delete=models.CASCADE )
    online_status = models.BooleanField(default=False)
    verify_status = models.BooleanField(default=False)
    chat_mute_status=models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    otp = models.CharField(max_length= 4,null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User,related_name='created_by', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_id)
   

class Countries(models.Model):
    country_name = models.CharField(max_length=50, null=True)
    
    country_tel_code= models.CharField(max_length=10, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User,related_name='country_created_by', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.country_name)


class UserType(models.Model):
    type_name = models.CharField(max_length=20,blank=True, null=True)
    image = models.ImageField(upload_to='usertype_img', blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User,related_name='usertype_created_by', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.type_name)
