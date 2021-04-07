from django.contrib import admin
from .models import *
from django.contrib.admin.options import ModelAdmin
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class Product_categoryAdmin(ModelAdmin):
    list_display = ["category_name","created_dt","created_by","slug"]
admin.site.register(Product_category, Product_categoryAdmin)

class Product_subcategoryAdmin(ModelAdmin):
    list_display = ["product_category_id","subcategory_name","created_dt","created_by","slug"]
admin.site.register(Product_subcategory, Product_subcategoryAdmin)
#
#
class Fabric_typeAdmin(ModelAdmin):
    list_display = ["name","created_dt","created_by"]
admin.site.register(Fabric_type, Fabric_typeAdmin)
#
class Washing_methodAdmin(ModelAdmin):
    list_display = ["name","image","created_dt","created_by"]
admin.site.register(Washing_method, Washing_methodAdmin)

class SeasonAdmin(ModelAdmin):
    list_display = ["season_name","created_dt","created_by"]
admin.site.register(Season, SeasonAdmin)

class Thread_typeAdmin(ModelAdmin):
    list_display = ["name","created_dt","created_by"]
admin.site.register(Thread_type, Thread_typeAdmin)
#
class Material_type1Admin(ModelAdmin):
    list_display = ["name","created_dt","created_by"]
admin.site.register(Material_type1, Material_type1Admin)

class Material_type2Admin(ModelAdmin):
    list_display = ["name","created_dt","created_by"]
admin.site.register(Material_type2, Material_type2Admin)
#
class SupplierProductAdmin(ModelAdmin):
    list_display = ["user_id","product_category","Product_subcategory"]
admin.site.register(SupplierProduct,SupplierProductAdmin)


# class CountryCurrencyAdmin(ModelAdmin):
#     list_display = ["currency","unit_text","symbol"]
# admin.site.register(CountryCurrency,CountryCurrencyAdmin)


@admin.register(CountryCurrency)
class ViewAdmin(ImportExportModelAdmin):
    pass