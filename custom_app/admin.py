from django.contrib import admin
from .models import *
from django.contrib.admin.options import ModelAdmin
# Register your models here.

admin.site.register(AboutUs)



class CustomPageAdmin(ModelAdmin):
    list_display = ["page_name","slug"]
admin.site.register(CustomPage,CustomPageAdmin)