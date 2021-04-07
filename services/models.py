from django.db import models
from django.contrib.auth.models import User
import django

from account.models import Countries


class TailorSpecification(models.Model):
    tailor_speci=models.CharField(max_length=50, null=True, blank=True)
    img=models.ImageField(upload_to='services_images',null=True, blank=True)
    description=models.TextField(max_length=300, null=True, blank=True)
    status=models.BooleanField(default=True)
    created_dt = models.DateTimeField(default=django.utils.timezone.now)
    created_by = models.ForeignKey(User, related_name='tailor_speci_created_by', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.tailor_speci)

class TargetedCustomer(models.Model):
    name=models.CharField(max_length=50, null=True, blank=True)
    created_dt = models.DateTimeField(default=django.utils.timezone.now)
    created_by = models.ForeignKey(User, related_name='targetedcustomer_created_by', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class SupplierServices(models.Model):
    user_id = models.ForeignKey(User,  related_name='supplier_services',on_delete=models.CASCADE)
    country_id = models.ForeignKey(Countries, related_name='supplier_services_country', on_delete=models.CASCADE)
    tailor_speci_id = models.ForeignKey(TailorSpecification, related_name='supplier_tailor_speci', on_delete=models.CASCADE)
    tailor_experience = models.CharField(max_length=10, null=True, blank=True)
    targeted_customer =  models.ManyToManyField(TargetedCustomer,related_name='targeted_customer')
    tailor_staff_gender= models.ManyToManyField(TargetedCustomer,related_name='tailor_staff_gender')
    address = models.TextField(max_length=100, null=True, blank=True)
    status=models.BooleanField(default=True)
    ship_outside_country=models.BooleanField(default=False)
    created_dt = models.DateTimeField(default=django.utils.timezone.now)
    created_by = models.ForeignKey(User, related_name='services_created_by', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.tailor_speci_id)