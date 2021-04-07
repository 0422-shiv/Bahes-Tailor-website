from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from account.models import Countries
from autoslug import AutoSlugField

class Product_category(models.Model):
    category_name=models.CharField(max_length=30, null=True, blank=True)
    image = models.ImageField(upload_to='product_category_img', null=True, blank=True)
    created_dt = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, related_name='product_category_created_by', on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='category_name', null=True, blank=True)

    def __str__(self):
        return str(self.category_name)

class Product_subcategory(models.Model):
    product_category_id=models.ForeignKey(Product_category, related_name='product_category_id', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_category_img', null=True, blank=True)
    subcategory_name=models.CharField(max_length=50, null=True, blank=True)
    created_dt = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, related_name='Product_subcategory_created_by', on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='subcategory_name', null=True, blank=True)

    def __str__(self):
        return str(self.subcategory_name)

      

class Thread_type(models.Model):
    name=models.CharField(max_length=50, null=True, blank=True)
    created_dt = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class Fabric_type(models.Model):
    name=models.CharField(max_length=50, null=True, blank=True)
    created_dt = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, related_name='fabric_type_created_by', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)



class Washing_method(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='washing_method_img', null=True, blank=True)
    
    created_dt = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, related_name='washing_method_created_by', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
    

class Material_type1(models.Model):
    name=models.CharField(max_length=50, null=True, blank=True)
    created_dt = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, related_name='materials_type1_created_by', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class Material_type2(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_dt = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, related_name='materials_type2_created_by', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class Season(models.Model):
    season_name = models.CharField(max_length=100, null=True, blank=True)
    created_dt = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.season_name)

class SupplierProduct(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    product_category = models.ForeignKey(Product_category, on_delete=models.CASCADE, null=True, blank=True)
    Product_subcategory = models.ForeignKey(Product_subcategory, related_name='product_subcategory', on_delete=models.CASCADE, null=True, blank=True)
    country_origin = models.ForeignKey(Countries,  on_delete=models.CASCADE, null=True, blank=True)
    fabrictype = models.ForeignKey(Fabric_type, related_name='fabric_type', on_delete=models.CASCADE, null=True, blank=True)
    threadtype = models.ForeignKey(Thread_type, related_name='thread_type', on_delete=models.CASCADE, null=True, blank=True)
    material_type1 = models.ForeignKey(Material_type1, related_name='material_type1', on_delete=models.CASCADE, null=True, blank=True)
    material_type2 = models.ForeignKey(Material_type2, related_name='material_type2', on_delete=models.CASCADE, null=True, blank=True)
    color = models.TextField(null=True)
    currency=models.CharField(max_length=30, null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=3,null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    width_size= models.DecimalField(max_digits=20, decimal_places=3, null=True, blank=True)
    washing_method = models.ManyToManyField(Washing_method,null=True, blank=True)
    season = models.ManyToManyField(Season, null=True, blank=True)
    roller = models.CharField(max_length=30, null=True, blank=True)
    other_description = models.TextField( null=True, blank=True)
    image_1 = models.ImageField(upload_to='product_img', null=True, blank=True)
    image_2 = models.ImageField(upload_to='product_img', null=True, blank=True)
    
    created_dt = models.DateTimeField(default=timezone.now)
    
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.user_id)

class CountryCurrency(models.Model):
    currency=models.CharField(max_length=30, null=True, blank=True)
    unit_text=models.CharField(max_length=100, null=True, blank=True)
    symbol=models.CharField(max_length=30, null=True, blank=True)

    

   
    def __str__(self):
        return str(self.unit_text)