from django.contrib import admin
from .models import *
from django.contrib.admin.options import ModelAdmin


# Register your models here.


class TailorSpecificationAdmin(ModelAdmin):
    list_display = ["tailor_speci", "created_dt", "created_by"]


admin.site.register(TailorSpecification, TailorSpecificationAdmin)


class TargetedCustomerAdmin(ModelAdmin):
    list_display = ["name", "created_dt", "created_by"]


admin.site.register(TargetedCustomer, TargetedCustomerAdmin)


class SupplierServicesAdmin(ModelAdmin):
    list_display = ["user_id", "country_id", "tailor_speci_id", "tailor_experience", "status", "ship_outside_country",
                    "created_dt", "created_by"]


admin.site.register(SupplierServices, SupplierServicesAdmin)
