from django.contrib import admin
from .models import *
from django.contrib.admin.options import ModelAdmin
from import_export.admin import ImportExportModelAdmin
# Register your models here.

admin.site.register(UserProfile)
# admin.site.register(Countries)
admin.site.register(UserType)

@admin.register(Countries)
class ViewAdmin(ImportExportModelAdmin):
    pass