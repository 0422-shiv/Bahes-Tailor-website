from django.contrib import admin
from .models import *
from django.contrib.admin.options import ModelAdmin


# Register your models here.


class How_it_worksAdmin(ModelAdmin):
    list_display = ["title", "image", 'created_date',"created_by"]


admin.site.register(How_it_works, How_it_worksAdmin)


# class System_settingsAdmin(ModelAdmin):
#     list_display = ["logo",'header_bg_img','service_counter','product_counter','supplier_counter','about_image','about_title','about_description','fb','twitter','linkedin', "created_date", "created_by"]


admin.site.register(System_settings)


