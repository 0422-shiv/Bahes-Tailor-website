from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class BahesPayment(models.Model):
	user_id = models.ForeignKey(User,related_name='payment_user', on_delete=models.CASCADE)
	amount=models.CharField(max_length= 50, blank=True, null=True)
	payment_method=models.CharField(max_length= 50, blank=True, null=True)
	payment_status = models.BooleanField(default=False)
	payment_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return str(self.user_id)


class RegistraionFees(models.Model):
	amount=models.CharField(max_length= 50, blank=True, null=True)
	content=models.CharField(max_length= 200 ,blank=True, null=True)
  