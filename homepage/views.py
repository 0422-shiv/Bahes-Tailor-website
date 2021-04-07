
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views import generic
from admin_settings.models import System_settings,How_it_works
from account.models import UserProfile
from services.models import *
from products.models import *
from django.db.models import Count,Max
# Create your views here.
# @method_decorator(login_required, name="dispatch")
class HomePage(generic.TemplateView):
    template_name = 'homepage/index.html'

    def get(self, request, *args, **kwargs):
        get_how_it_works = How_it_works.objects.all()
        get_system_settings = System_settings.objects.all()
        get_services=TailorSpecification.objects.filter(status=True)
        
       
        get_supplier=SupplierServices.objects.filter(status=True).distinct('user_id')
       
        get_supplier_count=UserProfile.objects.all().filter(user_type__type_name='supplier').count()
        get_product_cat=get_object_or_404(Product_category,slug='fabrics')
        get_product_subcat=Product_subcategory.objects.all()
        get_products=SupplierProduct.objects.filter(status=True)
        return render(request, self.template_name,{'get_products':get_products,'get_product_subcat':get_product_subcat,'get_product_cat':get_product_cat,'get_services':get_services,'get_supplier_count':get_supplier_count,'get_how_it_works':get_how_it_works,'get_system_settings':get_system_settings,'get_supplier':get_supplier})



