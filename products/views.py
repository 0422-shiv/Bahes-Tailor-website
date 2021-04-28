from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from account.models import UserProfile
from django.contrib.auth.models import User, auth
from admin_settings.models import System_settings
from account.models import Countries
from services.models import TailorSpecification
import base64
from django.core.files.base import ContentFile
import simplejson as json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaulttags import register
from bahes.settings import BASE_URL

# @method_decorator(login_required(login_url='/account/login'))
@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class Product(generic.TemplateView):
    template_name = 'products/product.html'
    
    

    def get(self, request, *args, **kwargs):

        user_instance = get_object_or_404(User, id=request.user.id)
        userprofile_instance = get_object_or_404(UserProfile,user_id=user_instance)
        get_system_settings = System_settings.objects.all()
        get_supplier_product=SupplierProduct.objects.filter(user_id=user_instance).order_by('-id')
        get_product_cate=Product_category.objects.all()
       

        page = request.GET.get('page', 1)

        paginator = Paginator(get_supplier_product, 12)
        try:
            get_products = paginator.page(page)
        except PageNotAnInteger:
            get_products = paginator.page(1)
        except EmptyPage:
            get_products = paginator.page(paginator.num_pages)
            
        
        return render(request, self.template_name,{'get_products':get_products,'get_supplier_product':get_supplier_product,'get_product_cate':get_product_cate,'userprofile': userprofile_instance,'get_system_settings':get_system_settings})

    def post(self, request, *args, **kwargs):
        if 'user' in request.POST:
            if not request.POST['user']  == 'None' :
                user_profile_instance=get_object_or_404(UserProfile,id=request.POST['user'])
                user_instance=user_profile_instance.user_id
              
            else:
                user_instance=request.user

        if 'fabric' in request.POST:
            fabric=request.POST['fabric']
            get_fabric_instance=get_object_or_404(Product_category,id=fabric)
         
            country=request.POST['country']
            get_country=get_object_or_404(Countries,id=country)
            fabric_type=request.POST['fabric_type']
            get_fabrictype=get_object_or_404(Fabric_type,id=fabric_type)
            color=request.POST.getlist('color')
            currency=request.POST['currency']
        
            price=request.POST['price']
            quantity=request.POST['quantity']
            size=request.POST['size']
            
            description=request.POST['description']

            fabric_datasave=SupplierProduct(user_id=user_instance,product_category=get_fabric_instance,country_origin=get_country,fabrictype=get_fabrictype,currency=currency,price=price,quantity=quantity,width_size=size,other_description=description)
            fabric_datasave.color=json.dumps(color)
            fabric_datasave.save()

            if 'season' in request.POST:
                season=request.POST.getlist('season')
                for s in season:
                    get_season=get_object_or_404(Season,id=s)
                    
                    fabric_datasave.season.add(get_season)
                    fabric_datasave.save()
            if 'washing' in request.POST:
                washing_method=request.POST.getlist('washing')
                for w in washing_method:
                    get_washing_method=get_object_or_404(Washing_method,id=w)
                    fabric_datasave.washing_method.add(get_washing_method)
                    fabric_datasave.save()
            if request.POST["profilepic"] :
                    format, imgstr = request.POST["profilepic"].split(
                        ';base64,')
                    ext = format.split('/')[-1]

                    file_name = "first." + ext
                    data = ContentFile(
                        base64.b64decode(imgstr), name=file_name)
                    fabric_datasave.image_1=data
                    fabric_datasave.save()
                   
            if request.POST["fabric_product2"]:
                    format, imgstr = request.POST["fabric_product2"].split(
                            ';base64,')
                    ext = format.split('/')[-1]
                   
                    file_name = "second" + "." + ext
                    
                    data = ContentFile(
                        base64.b64decode(imgstr), name=file_name)
                    
                    fabric_datasave.image_2=data
                    fabric_datasave.save()
            messages.success(request, 'Product Successfully added')
        elif 'accessories' in request.POST:     
        
            accessories=request.POST['accessories']
            get_instance=get_object_or_404(Product_category,id=accessories)
            if 'thread' in request.POST:
                thread=request.POST['thread']
                get_sub_cat_instance=get_object_or_404(Product_subcategory,id=thread)
                thread_type=request.POST['thread_type']
                get_thread_type=get_object_or_404(Thread_type,id=thread_type)
                currency=request.POST['currency']
                price=request.POST['price']
                quantity=request.POST['quantity']
                description=request.POST['description']
                color=request.POST.getlist('color')
                datasave=SupplierProduct(user_id=user_instance,product_category=get_instance,Product_subcategory=get_sub_cat_instance,threadtype=get_thread_type,currency=currency,price=price,quantity=quantity,other_description=description)
                datasave.color=json.dumps(color)
                datasave.save()
                if request.POST["profilepic"] :
                    format, imgstr = request.POST["profilepic"].split(
                        ';base64,')
                    ext = format.split('/')[-1]

                    file_name = "first." + ext
                    data = ContentFile(
                        base64.b64decode(imgstr), name=file_name)
                    datasave.image_1=data
                    datasave.save()
                   
                if request.POST["fabric_product2"]:
                        format, imgstr = request.POST["fabric_product2"].split(
                                ';base64,')
                        ext = format.split('/')[-1]
                       
                        file_name = "second" + "." + ext
                        
                        data = ContentFile(
                            base64.b64decode(imgstr), name=file_name)
                        
                        datasave.image_2=data
                        datasave.save()
                messages.success(request, 'Product Successfully added')    
            elif 'buttons' in request.POST:
                buttons=request.POST['buttons']
                get_sub_cat_instance=get_object_or_404(Product_subcategory,id=buttons)
                material_type1=request.POST['material_type1']
                get_material_type1=get_object_or_404(Material_type1,id=material_type1)
                size=request.POST['size']
                country=request.POST['country']
                get_country=get_object_or_404(Countries,id=country)
                price=request.POST['price']
                currency=request.POST['currency']
                description=request.POST['description']
                color=request.POST.getlist('color')
                datasave=SupplierProduct(user_id=user_instance,product_category=get_instance,Product_subcategory=get_sub_cat_instance,material_type1=get_material_type1,width_size=size,country_origin=get_country,currency=currency,price=price,other_description=description)
                datasave.color=json.dumps(color)
                datasave.save()
                if request.POST["profilepic"] :
                    format, imgstr = request.POST["profilepic"].split(
                        ';base64,')
                    ext = format.split('/')[-1]

                    file_name = "first." + ext
                    data = ContentFile(
                        base64.b64decode(imgstr), name=file_name)
                    datasave.image_1=data
                    datasave.save()
                   
                if request.POST["fabric_product2"]:
                        format, imgstr = request.POST["fabric_product2"].split(
                                ';base64,')
                        ext = format.split('/')[-1]
                       
                        file_name = "second" + "." + ext
                        
                        data = ContentFile(
                            base64.b64decode(imgstr), name=file_name)
                        
                        datasave.image_2=data
                        datasave.save()
                messages.success(request, 'Product Successfully added')
            elif 'elastic' in request.POST:
                elastic=request.POST['elastic']
                get_sub_cat_instance=get_object_or_404(Product_subcategory,id=elastic)
                material_type2=request.POST['material_type2']
                get_material_type2=get_object_or_404(Material_type2,id=material_type2)
                country=request.POST['country']
                get_country=get_object_or_404(Countries,id=country)
                size=request.POST['size']
                price=request.POST['price']
                currency=request.POST['currency']
                roller=request.POST['roller']
                description=request.POST['description']
                color=request.POST.getlist('color')
                datasave=SupplierProduct(user_id=user_instance,product_category=get_instance,Product_subcategory=get_sub_cat_instance,material_type2=get_material_type2,country_origin=get_country,width_size=size,currency=currency,price=price,roller=roller,other_description=description)
                datasave.color=json.dumps(color)
                datasave.save()
                if request.POST["profilepic"] :
                    format, imgstr = request.POST["profilepic"].split(
                        ';base64,')
                    ext = format.split('/')[-1]

                    file_name = "first." + ext
                    data = ContentFile(
                        base64.b64decode(imgstr), name=file_name)
                    datasave.image_1=data
                    datasave.save()
                   
                if request.POST["fabric_product2"]:
                        format, imgstr = request.POST["fabric_product2"].split(
                                ';base64,')
                        ext = format.split('/')[-1]
                       
                        file_name = "second" + "." + ext
                        
                        data = ContentFile(
                            base64.b64decode(imgstr), name=file_name)
                        
                        datasave.image_2=data
                        datasave.save()
                messages.success(request, 'Product Successfully added')
            else:
                messages.error(request, ' products can not be add', )
        if request.user.is_superuser:
            id=str(user_profile_instance.id)      
            return redirect(BASE_URL+'admin/manage-member/view-products/'+id)
        else:
            return HttpResponseRedirect(reverse('products:product'))
            
           
            
@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class GetProductCategory(generic.TemplateView):
   

    def get(self, request,id, *args, **kwargs):
        if 'userid' in request.GET:
            userid=request.GET['userid']
        else:
            userid=None
        get_countries=Countries.objects.all()

        get_product_subcate=None
        get_product_cate=get_object_or_404(Product_category,id=id)
        if Product_subcategory.objects.filter(product_category_id=get_product_cate).exists():
            
            get_product_subcate=Product_subcategory.objects.filter(product_category_id=get_product_cate)
            return render(request, 'products/product-sub-category.html',{'userid':userid,'get_countries':get_countries,'get_product_subcate':get_product_subcate})       
        elif get_product_cate.slug ==   'fabrics':
            get_currency=CountryCurrency.objects.all()
            get_fabric_type=Fabric_type.objects.all()
            get_washing_method=Washing_method.objects.all()
            get_season=Season.objects.all()
            return render(request, 'products/fabric.html',{'userid':userid,'get_currency':get_currency,'get_season':get_season,'get_washing_method':get_washing_method,'get_fabric_type':get_fabric_type,'get_countries':get_countries,'get_product_cate':get_product_cate})       


           
        
        
@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class GetSubProductCategory(generic.TemplateView):
 
    def get(self, request,id,slug, *args, **kwargs):
        if 'userid' in request.GET:
            userid=request.GET['userid']
        else:
            userid=None
        get_countries=Countries.objects.all()
        get_currency=CountryCurrency.objects.all()
       
        get_sub_cat_instance=get_object_or_404(Product_subcategory,id=id)
        if get_sub_cat_instance.slug == 'threads':
            get_thread_type=Thread_type.objects.all()
            return render(request, 'products/thread.html',{'userid':userid,'get_currency':get_currency,'get_thread_type':get_thread_type,'id':id,'get_countries':get_countries,'get_sub_cat_instance':get_sub_cat_instance})       

        elif get_sub_cat_instance.slug == 'buttons-and-closures':
            get_material_type1=Material_type1.objects.all()
            return render(request, 'products/buttons.html',{'userid':userid,'get_currency':get_currency,'get_material_type1':get_material_type1,'id':id,'get_countries':get_countries,'get_sub_cat_instance':get_sub_cat_instance})       

        
        elif get_sub_cat_instance.slug == 'zipperstapetrim-and-elastic':
            get_material_type2=Material_type2.objects.all()
            return render(request, 'products/elastic.html',{'userid':userid,'get_currency':get_currency,'get_material_type2':get_material_type2,'id':id,'get_countries':get_countries,'get_sub_cat_instance':get_sub_cat_instance})       

@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class ProductDelete(generic.TemplateView):

    def post(self, request, id, *args, **kwargs):

        product_instance = get_object_or_404(SupplierProduct, id=id)
        user_instance = get_object_or_404(User, id=product_instance.user_id.id)
        SupplierProduct.objects.filter(id=product_instance.id).delete()
        if request.user.is_superuser:
            id=str(user_instance.userx.id)      
            return redirect(BASE_URL+'admin/manage-member/view-products/'+id)
        else:
            return HttpResponseRedirect(reverse('products:product'))
       
           
@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class ProductStatus(generic.TemplateView):
    template_name = 'products/product.html'

    def post(self, request, *args, **kwargs):

        productid = request.POST["productid"]
        productstatus = request.POST["productstatus"]

        if productstatus == "True":
            status = False
        else:
            status = True
        if SupplierProduct.objects.filter(id=productid).exists():
            # service_instance = get_object_or_404(SupplierServices, id=serviceid)
            SupplierProduct.objects.filter(id=productid).update(status=status)
        return JsonResponse({'message': 'Status Changed successfully.'})

            
            

@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class ProductEdit(generic.TemplateView):
   
    def get(self, request,id, *args, **kwargs):
        get_countries=Countries.objects.all()
        product_instance = get_object_or_404(SupplierProduct,id=id)
        user_instance = get_object_or_404(User, id=product_instance.user_id.id)
        userprofile = UserProfile.objects.get(user_id=user_instance)
        jsonDec = json.decoder.JSONDecoder()
        get_color_list = jsonDec.decode(product_instance.color)
        get_currency=CountryCurrency.objects.all()
        if product_instance.product_category.slug == 'fabrics':
            season=product_instance.season.all()
            get_fabric_type=Fabric_type.objects.all()
            get_washing_method=Washing_method.objects.all()
            get_season=Season.objects.all()
            washing_method=product_instance.washing_method.all()
            return render(request, 'products/edit-fabric.html',
                          {'get_currency':get_currency,'get_color_list':get_color_list,'season':season,'washing_method':washing_method,'get_season':get_season,'get_washing_method':get_washing_method, 'get_fabric_type':get_fabric_type,'get_countries':get_countries,'product_instance':product_instance, 'userprofile': userprofile,'user_instance': user_instance})

        elif product_instance.product_category.slug == 'sewing-yar-and-accessories':
            if product_instance.Product_subcategory.slug == 'threads':
                get_thread_type=Thread_type.objects.all()
                return render(request, 'products/edit-thread.html',{'get_currency':get_currency,'get_color_list':get_color_list,'product_instance':product_instance,'get_thread_type':get_thread_type})
            elif product_instance.Product_subcategory.slug == 'buttons-and-closures':
                get_material_type1=Material_type1.objects.all()
                return render(request, 'products/edit-buttons.html',{'get_currency':get_currency,'get_color_list':get_color_list,'product_instance':product_instance,'get_countries':get_countries,'get_material_type1':get_material_type1})

            elif product_instance.Product_subcategory.slug == 'zipperstapetrim-and-elastic':
                get_material_type2=Material_type2.objects.all()
                return render(request, 'products/edit-elastic.html',{'get_currency':get_currency,'get_color_list':get_color_list,'product_instance':product_instance,'get_countries':get_countries,'get_material_type2':get_material_type2})

    def post(self, request,id, *args, **kwargs):
        
        if SupplierProduct.objects.filter(id=id).exists:
            product_instance = get_object_or_404(SupplierProduct,id=id)
            user_instance=get_object_or_404(User,id=product_instance.user_id.id)
           
            if 'fabric' in request.POST:
                fabric=request.POST['fabric']
                get_fabric_instance=get_object_or_404(Product_category,id=fabric)
             
                country=request.POST['country']
                get_country=get_object_or_404(Countries,id=country)
                fabric_type=request.POST['fabric_type']
                get_fabrictype=get_object_or_404(Fabric_type,id=fabric_type)
                color=request.POST.getlist('color')
                currency=request.POST['currency']
                price=request.POST['price']
                quantity=request.POST['quantity']
                size=request.POST['size']
                
                description=request.POST['description']

                product_instance.color=json.dumps(color)
                product_instance.save()

                if 'season' in request.POST:
                    season=request.POST.getlist('season')
                    product_instance.season.set(season)

                if 'washing' in request.POST:
                    washing_method=request.POST.getlist('washing')
                    product_instance.washing_method.set(washing_method)
                    
                if request.POST["profilepic"] :
                        format, imgstr = request.POST["profilepic"].split(
                            ';base64,')
                        ext = format.split('/')[-1]

                        file_name = "first." + ext
                        data = ContentFile(
                            base64.b64decode(imgstr), name=file_name)
                        product_instance.image_1=data
                        product_instance.save()
                       
                if request.POST["fabric_product2"]:
                        format, imgstr = request.POST["fabric_product2"].split(
                                ';base64,')
                        ext = format.split('/')[-1]
                       
                        file_name = "second" + "." + ext
                        
                        data = ContentFile(
                            base64.b64decode(imgstr), name=file_name)
                        
                        product_instance.image_2=data
                        product_instance.save()
                SupplierProduct.objects.filter(id=id).update(user_id=user_instance,product_category=get_fabric_instance,country_origin=get_country,fabrictype=get_fabrictype,currency=currency,price=price,quantity=quantity,width_size=size,other_description=description)

                messages.success(request, 'Product Successfully Edited')
            elif 'accessories' in request.POST:     
            
                accessories=request.POST['accessories']
                get_instance=get_object_or_404(Product_category,id=accessories)
                if 'thread' in request.POST:
                    thread=request.POST['thread']
                    get_sub_cat_instance=get_object_or_404(Product_subcategory,id=thread)
                    thread_type=request.POST['thread_type']
                    get_thread_type=get_object_or_404(Thread_type,id=thread_type)
                    currency=request.POST['currency']
                    price=request.POST['price']
                    quantity=request.POST['quantity']
                    description=request.POST['description']
                    color=request.POST.getlist('color')
                    product_instance.color=json.dumps(color)
                    product_instance.save()
                    if request.POST["profilepic"] :
                        format, imgstr = request.POST["profilepic"].split(
                            ';base64,')
                        ext = format.split('/')[-1]

                        file_name = "first." + ext
                        data = ContentFile(
                            base64.b64decode(imgstr), name=file_name)
                        product_instance.image_1=data
                        product_instance.save()
                       
                    if request.POST["fabric_product2"]:
                            format, imgstr = request.POST["fabric_product2"].split(
                                    ';base64,')
                            ext = format.split('/')[-1]
                           
                            file_name = "second" + "." + ext
                            
                            data = ContentFile(
                                base64.b64decode(imgstr), name=file_name)
                            
                            product_instance.image_2=data
                            product_instance.save()
                    SupplierProduct.objects.filter(id=id).update(user_id=user_instance,product_category=get_instance,Product_subcategory=get_sub_cat_instance,threadtype=get_thread_type,currency=currency,price=price,quantity=quantity,other_description=description)

                    messages.success(request, 'Product Successfully Edited')    
                elif 'buttons' in request.POST:
                    buttons=request.POST['buttons']
                    get_sub_cat_instance=get_object_or_404(Product_subcategory,id=buttons)
                    material_type1=request.POST['material_type1']
                    get_material_type1=get_object_or_404(Material_type1,id=material_type1)
                    size=request.POST['size']
                    country=request.POST['country']
                    get_country=get_object_or_404(Countries,id=country)
                    currency=request.POST['currency']
                    price=request.POST['price']
                    description=request.POST['description']
                    color=request.POST.getlist('color')
                    product_instance.color=json.dumps(color)
                    product_instance.save()
                    if request.POST["profilepic"] :
                        format, imgstr = request.POST["profilepic"].split(
                            ';base64,')
                        ext = format.split('/')[-1]

                        file_name = "first." + ext
                        data = ContentFile(
                            base64.b64decode(imgstr), name=file_name)
                        product_instance.image_1=data
                        product_instance.save()
                       
                    if request.POST["fabric_product2"]:
                            format, imgstr = request.POST["fabric_product2"].split(
                                    ';base64,')
                            ext = format.split('/')[-1]
                           
                            file_name = "second" + "." + ext
                            
                            data = ContentFile(
                                base64.b64decode(imgstr), name=file_name)
                            
                            product_instance.image_2=data
                            product_instance.save()
                    SupplierProduct.objects.filter(id=id).update(user_id=user_instance,product_category=get_instance,Product_subcategory=get_sub_cat_instance,material_type1=get_material_type1,width_size=size,country_origin=get_country,currency=currency,price=price,other_description=description)

                    messages.success(request, 'Product Successfully Edited')
                elif 'elastic' in request.POST:
                    elastic=request.POST['elastic']
                    get_sub_cat_instance=get_object_or_404(Product_subcategory,id=elastic)
                    material_type2=request.POST['material_type2']
                    get_material_type2=get_object_or_404(Material_type2,id=material_type2)
                    country=request.POST['country']
                    get_country=get_object_or_404(Countries,id=country)
                    size=request.POST['size']
                    currency=request.POST['currency']
                    price=request.POST['price']
                    roller=request.POST['roller']
                    description=request.POST['description']
                    
                    color=request.POST.getlist('color')
                    product_instance.color=json.dumps(color)
                    product_instance.save()
                    if request.POST["profilepic"] :
                        format, imgstr = request.POST["profilepic"].split(
                            ';base64,')
                        ext = format.split('/')[-1]

                        file_name = "first." + ext
                        data = ContentFile(
                            base64.b64decode(imgstr), name=file_name)
                        product_instance.image_1=data
                        product_instance.save()
                       
                    if request.POST["fabric_product2"]:
                            format, imgstr = request.POST["fabric_product2"].split(
                                    ';base64,')
                            ext = format.split('/')[-1]
                           
                            file_name = "second" + "." + ext
                            
                            data = ContentFile(
                                base64.b64decode(imgstr), name=file_name)
                            
                            product_instance.image_2=data
                            product_instance.save()
                    SupplierProduct.objects.filter(id=id).update(user_id=user_instance,product_category=get_instance,Product_subcategory=get_sub_cat_instance,material_type2=get_material_type2,country_origin=get_country,width_size=size,currency=currency,price=price,roller=roller,other_description=description)

                    messages.success(request, 'Product Successfully Edited')
                else:
                    messages.error(request, ' products can not be Edited', )
        if request.user.is_superuser:
            id=str(user_instance.userx.id)      
            return redirect(BASE_URL+'admin/manage-member/view-products/'+id)
        else:
            return HttpResponseRedirect(reverse('products:product'))

@register.filter(name='total_myproducts_counter')
def total_myproducts_counter(user):
    total_myproducts_counter = 0
    if User.objects.filter(id=user.id).exists():
        user_instance = get_object_or_404(User, id=user.id)
        userprofile_instance = get_object_or_404(UserProfile,user_id=user_instance)
        total_myproducts_counter = SupplierProduct.objects.filter(user_id=user_instance).count()
    
    return total_myproducts_counter       