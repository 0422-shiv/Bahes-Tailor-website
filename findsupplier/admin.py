from django.contrib import admin
from .models import *
from django.contrib.admin.options import ModelAdmin

class BahesPaymentAdmin(ModelAdmin):
    list_display = ["user_id","amount","payment_method","payment_status","payment_date"]
admin.site.register( BahesPayment,BahesPaymentAdmin)
