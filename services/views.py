from django.shortcuts import render, HttpResponse, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views import generic
from django.db.models import Q
from account.models import UserProfile
from services.forms import SupplierServicesForm
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from bahes.settings import BASE_URL
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from admin_settings.models import System_settings
from django.template.defaulttags import register


@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class Services(generic.TemplateView):
    template_name = 'services/services.html'
 
    def get(self, request,  *args, **kwargs):
        get_services = SupplierServices.objects.filter(user_id=request.user).order_by('-id')
        get_system_settings = System_settings.objects.all()
        return render(request, self.template_name,
                      {'get_system_settings':get_system_settings,'get_services': get_services,})


  
@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class PostServices(generic.TemplateView):
    template_name = 'services/post-services.html' 
    form = SupplierServicesForm  
    def get(self, request,  *args, **kwargs): 
        get_system_settings = System_settings.objects.all()
        get_tailor_spec=TailorSpecification.objects.filter(status=True)
        userprofile_instance = get_object_or_404(UserProfile,user_id=request.user)
        return render(request, self.template_name,
                      {'get_system_settings':get_system_settings,'form': self.form,'get_tailor_spec':get_tailor_spec,'userprofile':userprofile_instance})
    

    def post(self, request,  *args, **kwargs):
        phone = request.POST['phone']
        tailor_spec = request.POST['tailor_spec']
        get_tailor_spec_instance=get_object_or_404(TailorSpecification,id=tailor_spec)
        user_instance = get_object_or_404(User,id=request.user.id)
        userprofile_instance = get_object_or_404(UserProfile,user_id=user_instance)
        if UserProfile.objects.filter(phone=phone).filter(~Q(user_id=user_instance)).exists():
            messages.error(request, phone + ' Phone number already exists', )
        elif SupplierServices.objects.filter(tailor_speci_id=get_tailor_spec_instance).filter(Q(user_id=user_instance)).exists():
            messages.error(request, 'Dear '+userprofile_instance.full_name+',you already have added '+ get_tailor_spec_instance.tailor_speci, )
        else:
            num = ""
            for c in request.POST['tel_code']:
                if c.isdigit():
                    num = num + c
            userprofile_instance.tel_code = num
            userprofile_instance.phone = phone
            userprofile_instance.save()
            get_supplierservices_form = self.form(request.POST)
          
            if get_supplierservices_form.is_valid():
                saveservices_data = get_supplierservices_form.save(commit=False)
                if 'yes' == request.POST['flexRadioDefault']:
                    saveservices_data.ship_outside_country = "True"
                else:
                    saveservices_data.ship_outside_country = "False"

                saveservices_data.user_id = request.user
                saveservices_data.created_by = request.user
                saveservices_data.tailor_speci_id=get_tailor_spec_instance
                saveservices_data.save()
                get_supplierservices_form.save_m2m()
                messages.success(request, 'Service is added Successfully ')
            else:
                messages.error(request, ' Services can not be added', )
       
        return HttpResponseRedirect(reverse('services:PostServices'))

@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class EditService(generic.TemplateView):
    template_name = 'services/edit.html'
    form = SupplierServicesForm

    def get(self, request,id, *args, **kwargs):

        service_instance = get_object_or_404(SupplierServices,id=id)
        form = SupplierServicesForm(instance=service_instance)
        user_instance = get_object_or_404(User, id=service_instance.user_id.id)
        userprofile = UserProfile.objects.get(user_id=user_instance)
        get_tailor_spec=TailorSpecification.objects.filter(status=True)
        return render(request, self.template_name,
                      {'get_tailor_spec':get_tailor_spec,'form': form, 'service_instance':service_instance, 'userprofile': userprofile,'user_instance': user_instance})


    def post(self, request, id, *args, **kwargs):
        
        phone = request.POST['phone']
        tailor_spec = request.POST['tailor_spec']
        get_tailor_spec_instance=get_object_or_404(TailorSpecification,id=tailor_spec)
        service_instance = get_object_or_404(SupplierServices, id=id)
        user_instance = get_object_or_404(User, id=service_instance.user_id.id)
        userprofile_instance = get_object_or_404(UserProfile, user_id=user_instance)
        if UserProfile.objects.filter(phone=phone).filter(~Q(user_id=user_instance)).exists():
            messages.error(request, phone + ' Phone number already exists', )
        elif SupplierServices.objects.filter(tailor_speci_id=get_tailor_spec_instance).filter(Q(user_id=user_instance)).filter(~Q(id=id)).exists():
            messages.error(request, 'Dear '+userprofile_instance.full_name+',you already have added '+ get_tailor_spec_instance.tailor_speci, )
        else:

           
            userprofile_instance.phone = phone
            userprofile_instance.save()
            get_supplierservices_form = self.form(request.POST or None ,instance=service_instance)

            if get_supplierservices_form.is_valid():

                saveservices_data = get_supplierservices_form.save(commit=False)

                if 'yes' == request.POST['flexRadioDefault']:
                    saveservices_data.ship_outside_country = "True"
                else:
                    saveservices_data.ship_outside_country = "False"

                saveservices_data.user_id = user_instance
                saveservices_data.created_by = request.user
                saveservices_data.tailor_speci_id=get_tailor_spec_instance
                saveservices_data.save()
                get_supplierservices_form.save_m2m()
                messages.success(request, 'Services Successfully edited')
            else:
                messages.error(request, ' Services can not be edit', )
        if request.user.is_superuser:
            id=str(userprofile_instance.id)      
            return redirect(BASE_URL+'admin/manage-member/view-services/'+id)
        else:
            return HttpResponseRedirect(reverse('services:Services'))
      

@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class ServiceDelete(generic.TemplateView):

    def post(self, request, id, *args, **kwargs):

        service_instance = get_object_or_404(SupplierServices, id=id)
        user_instance = get_object_or_404(User, id=service_instance.user_id.id)
        SupplierServices.objects.filter(id=service_instance.id).delete()
        if request.user.is_superuser:
            id=str(user_instance.userx.id)      
            return redirect(BASE_URL+'admin/manage-member/view-services/'+id)
        else:
            return HttpResponseRedirect(reverse('services:Services'))


@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class ServiceStatus(generic.TemplateView):
    template_name = 'services/my-services.html'

    def post(self, request, *args, **kwargs):

        serviceid = request.POST["serviceid"]
        servicestatus = request.POST["servicestatus"]

        if servicestatus == "True":
            status = False
        else:
            status = True
        if SupplierServices.objects.filter(id=serviceid).exists():
            # service_instance = get_object_or_404(SupplierServices, id=serviceid)
            SupplierServices.objects.filter(id=serviceid).update(status=status)
        return JsonResponse({'message': 'Status Changed successfully.'})




@register.filter(name='total_myservices_counter')
def total_myservices_counter(user):
    total_myservices_counter = 0
    if User.objects.filter(id=user.id).exists():
        user_instance = get_object_or_404(User, id=user.id)
        userprofile_instance = get_object_or_404(UserProfile,user_id=user_instance)
        total_myservices_counter = SupplierServices.objects.filter(user_id=user_instance).count()
    
    return total_myservices_counter