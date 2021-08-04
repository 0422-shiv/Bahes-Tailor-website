
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views import generic
from admin_settings.models import System_settings,How_it_works
from account.models import UserProfile
from services.models import *
from products.models import *
from django.db.models import Count,Max
from collections import Counter
from django.db.models import Subquery
from django.template.defaulttags import register
from bahes import settings
from django.db.models import Q
from django.template.loader import render_to_string
from bahes.settings import BASE_URL

# Create your views here.
# @method_decorator(login_required, name="dispatch")
class HomePage(generic.TemplateView):
    template_name = 'homepage/index.html'

    def get(self, request, *args, **kwargs):
        if 'paymentdone' in request.GET:
            paymentdone=request.GET['paymentdone']
        else:
            paymentdone=''
        get_how_it_works = How_it_works.objects.all()
        get_system_settings = System_settings.objects.all()
        get_tailor_services=TailorSpecification.objects.filter(status=True)
        get_q=Q(supplier_tailor_speci__status=True)
        get_tailor_service=TailorSpecification.objects.annotate(service_count=Count('supplier_tailor_speci',get_q))
     
        get_tailor_service_list=[]
        for data in get_tailor_service:
            get_tailor_service_list.append(data.service_count)
        get_tailor_service_list = list(dict.fromkeys(get_tailor_service_list))
        get_tailor_service_list.sort(reverse=True)
        
        get_supplier=SupplierServices.objects.filter(status=True).distinct('user_id')
        get_supplier_count=UserProfile.objects.all().filter(user_type__type_name='supplier').count()
        get_product_cat=get_object_or_404(Product_category,slug='fabrics')
        get_product_subcat=Product_subcategory.objects.all()
        get_products=SupplierProduct.objects.filter(status=True)
        return render(request, self.template_name,{'BASE_URL':BASE_URL,'paymentdone':paymentdone,'get_tailor_service':get_tailor_service,'get_tailor_service_list':get_tailor_service_list,'get_products':get_products,'get_product_subcat':get_product_subcat,'get_product_cat':get_product_cat,'get_tailor_services':get_tailor_services,'get_supplier_count':get_supplier_count,'get_how_it_works':get_how_it_works,'get_system_settings':get_system_settings,'get_supplier':get_supplier})



@register.filter(name='get_footer_services')
def get_banner_img(footer_services):
    get_tailor_service=None
    if 'footer_services' == footer_services:
        if TailorSpecification.objects.all().exists():
            get_q=Q(supplier_tailor_speci__status=True)

            get_tailor_service=TailorSpecification.objects.annotate(service_count=Count('supplier_tailor_speci',get_q))
            get_tailor_service_list=[]
            for data in get_tailor_service:
                get_tailor_service_list.append(data.service_count)
            get_tailor_service_list = list(dict.fromkeys(get_tailor_service_list))
            get_tailor_service_list.sort(reverse=True)
            # print(get_tailor_service_list)
    return render_to_string('homepage/footer-services.html',{'get_tailor_service':get_tailor_service,'get_tailor_service_list':get_tailor_service_list})


@register.filter(name='get_banner_img')
def get_banner_img(demo):
    banner_image = settings.BASE_URL+"static/images/banner.png"
  
    if 'Home' == demo:
        if System_settings.objects.all().exists():
            get_data = System_settings.objects.all().first()
            if get_data.header_bg_img:
                banner_image = get_data.header_bg_img.url
    elif 'findsupplier' == demo:
        if System_settings.objects.all().exists():
            get_data = System_settings.objects.all().first()
            if get_data.find_supplier_bg_img:
                banner_image = get_data.find_supplier_bg_img.url
    elif 'FindServices' == demo:
        if System_settings.objects.all().exists():
            get_data = System_settings.objects.all().first()
            if get_data.find_services_bg_img:
                banner_image = get_data.find_services_bg_img.url
    elif 'FindProducts' == demo:
        if System_settings.objects.all().exists():
            get_data = System_settings.objects.all().first()
            if get_data.find_products_bg_img:
                banner_image = get_data.find_products_bg_img.url
    elif 'supplierdashboard' == demo:
        if System_settings.objects.all().exists():
            get_data = System_settings.objects.all().first()
            if get_data.supplier_dashboard_bg_img:
                banner_image = get_data.supplier_dashboard_bg_img.url
    elif 'customerdashboard' == demo:
        if System_settings.objects.all().exists():
            get_data = System_settings.objects.all().first()
            if get_data.customer_dashbaord_bg_img:
                banner_image = get_data.customer_dashbaord_bg_img.url
    # elif 'aboutus' == demo:
    #     if System_settings.objects.all().exists():
    #         get_data = System_settings.objects.all().first()
    #         if get_data.about_us_bg_img:
    #             banner_image = get_data.about_us_bg_img.url


    return str(banner_image)