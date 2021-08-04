from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
import base64
from django.core.files.base import ContentFile
from django.contrib.auth import update_session_auth_hash
from account.models import *
from account.forms import MyPasswordChangeForm
from bahes.settings import BASE_URL
from admin_settings.models import System_settings
from django.http import JsonResponse
from django.template.defaulttags import register
from findsupplier.models import *
from products.models import *
from services.models import *
from survey.models import *

@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class Dashboard(generic.TemplateView):
    template_name = 'dashboard/dashboard.html'
    def get(self, request, *args, **kwargs):
        user_instance = get_object_or_404(User, id=request.user.id)
        if UserProfile.objects.filter(user_id=user_instance).exists():
            userprofile_instance = get_object_or_404(UserProfile,user_id=user_instance)
            if not userprofile_instance.user_type == None :
                    if not UserAnswerTable.objects.filter(user=request.user).exists():
                        return redirect(BASE_URL + 'survey/' + str(request.user.userx.id)+'?q=1')
                    elif UserAnswerTable.objects.filter(user=request.user).exists():
                        if request.user.userx.user_type.type_name == 'supplier':
                            if not (UserAnswerTable.objects.filter(user=request.user).count()) == 4:
                                UserAnswerTable.objects.filter(user=request.user).delete()
                                return redirect(BASE_URL + 'survey/' + str(request.user.userx.id)+'?q=1')
                        else:
                            if not (UserAnswerTable.objects.filter(user=request.user).count()) == 2:
                                UserAnswerTable.objects.filter(user=request.user).delete()
                                return redirect(BASE_URL + 'survey/' + str(request.user.userx.id)+'?q=1')
            else:
                return HttpResponseRedirect(reverse('account:UserType'))

        else:
            return HttpResponseRedirect(reverse('account:UserType'))
        get_system_settings = System_settings.objects.all()
        get_supplier_product=SupplierProduct.objects.filter(user_id=user_instance).order_by('-id')
        get_services = SupplierServices.objects.filter(user_id=user_instance).order_by('-id')
        return render(request, self.template_name,{'get_system_settings':get_system_settings,'userprofile_instance':userprofile_instance,'get_supplier_product':get_supplier_product,'get_services':get_services})

@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class EditProfile(generic.TemplateView):
    # template_name = 'dashboard/profile.html'
    template_name = 'dashboard/update-profile.html'
    


    def get(self, request, *args, **kwargs):
        get_system_settings = System_settings.objects.all()
        user_instance = get_object_or_404(User, id=request.user.id)
        get_countries=Countries.objects.all()
        if UserProfile.objects.filter(user_id=user_instance).exists():
            userprofile_instance = get_object_or_404(UserProfile,user_id=user_instance)
            if not userprofile_instance.user_type == None :
                if not UserAnswerTable.objects.filter(user=request.user).exists():
                    return redirect(BASE_URL + 'survey/' + str(request.user.userx.id)+'?q=1')
                elif UserAnswerTable.objects.filter(user=request.user).exists():
                    if request.user.userx.user_type.type_name == 'supplier':
                        if not (UserAnswerTable.objects.filter(user=request.user).count()) == 4:
                            UserAnswerTable.objects.filter(user=request.user).delete()
                            return redirect(BASE_URL + 'survey/' + str(request.user.userx.id)+'?q=1')
                    else:
                        if not (UserAnswerTable.objects.filter(user=request.user).count()) == 2:
                            UserAnswerTable.objects.filter(user=request.user).delete()
                            return redirect(BASE_URL + 'survey/' + str(request.user.userx.id)+'?q=1')
            else:
                return HttpResponseRedirect(reverse('account:UserType'))

        else:
            return HttpResponseRedirect(reverse('account:UserType'))

        return render(request, self.template_name,{'userprofile': userprofile_instance,'get_system_settings':get_system_settings,'get_countries':get_countries})


    def post(self, request, *args, **kwargs):
        user_instance = get_object_or_404(User, id=request.user.id)
        if UserProfile.objects.filter(user_id=user_instance).exists():
            phone = request.POST["phone"]
            country = request.POST["country"]
            get_country=get_object_or_404(Countries,id=country)
            if UserProfile.objects.filter(phone=phone).filter(~Q(user_id=user_instance)).exists():
                messages.error(request, phone + ' Phone number already exists', )
            else:

                userupdate = get_object_or_404(UserProfile, user_id=user_instance)
                userupdate.full_name = request.POST["full_name"]
                userupdate.phone = request.POST["phone"]
                userupdate.country = get_country
                num = ""
                for c in request.POST['tel_code']:
                    if c.isdigit():
                        num = num + c
                userupdate.tel_code = num

                userupdate.save()
                messages.success(request, 'Profile Updated Successfully')
        return HttpResponseRedirect(reverse('dashboard:EditProfile'))
        # elif 'old_password' in  request.POST:
        #     messages.warning(request, 'change_password')
        #     flag='change_password'
        #     form = MyPasswordChangeForm(request.user, request.POST)

        #     if form.is_valid():
        #         user = form.save()
        #         update_session_auth_hash(request, user)  # Important!
        #         messages.success(request, 'Your password was successfully updated!')

        #     else:
        #         messages.error(request, 'Please correct the error below.')
      
        # else:
        #     flag='profile'
        #     messages.error(request, 'Something going wrong ,please try again')

      
        # return redirect(BASE_URL+'dashboard/profile/?flag='+flag)
     
@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class Updatepassword(generic.TemplateView):
    template_name = 'dashboard/update-password.html'
    def get(self, request, *args, **kwargs):
        get_system_settings = System_settings.objects.all()
        form = MyPasswordChangeForm(request.user)
        return render(request, self.template_name,{'get_system_settings':get_system_settings,'form':form})
    def post(self, request, *args, **kwargs):
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Password updated successfully !')

        else:
            messages.error(request, 'Please correct the error below.')
        return HttpResponseRedirect(reverse('dashboard:Updatepassword'))



@login_required
def ProfileChange(request):
    if request.method == 'POST':
        
        if 'save_profile_image' in request.POST:
          
            userupdate = get_object_or_404(UserProfile,user_id=get_object_or_404(User, id=request.user.id))
            format, imgstr = request.POST["save_profile_image"].split(';base64,')
            ext = format.split('/')[-1]

            file_name = "photo." + ext
            data = ContentFile(
                base64.b64decode(imgstr), name=file_name)


            userupdate.image = data
            userupdate.save()
            messages.success(request, 'Your profile pic was successfully updated!')
        else:
            messages.error(request, 'Something going wrong ,please try again')
        # if request.POST['pagename'] == 'profile':
        #      return HttpResponseRedirect(reverse('dashboard:EditProfile'))
        # elif request.POST['pagename'] == 'chat':
        #     return redirect(BASE_URL+"chat/?chatbahesroom=chatbahesroom")
        # elif request.POST['pagename'] == 'service':
        #     return HttpResponseRedirect(reverse('services:Services'))
        # elif request.POST['pagename'] == 'product':
        return HttpResponseRedirect(reverse('products:product'))



@login_required
def OnlineStatus(request):
   
        if request.method == 'POST': 
            onlinestatus = request.POST["onlinestatus"]
            userid = request.POST["userid"]
            print(onlinestatus,userid)
            if onlinestatus == "True":
                status = False
            else:
                status = True
            if UserProfile.objects.filter(id=userid).exists():
                print(status)
                UserProfile.objects.filter(id=userid).update(online_status=status)
                print((get_object_or_404(UserProfile,id=userid)).online_status)
            return JsonResponse({'message': 'Status Changed successfully.'})
        # return HttpResponseRedirect(reverse('dashboard:EditProfile'))



@register.filter(name='get_paid_status')
def get_paid_status(user):
    get_paid_status = False
    if BahesPayment.objects.filter(user_id=user.user_id).exists():
            get_user_ins=get_object_or_404(BahesPayment,user_id=user.user_id)
            get_paid_status=get_user_ins.payment_status
              
    return get_paid_status


@register.filter(name='get_service_counter')
def get_service_counter(user_id):
    get_service_count = 0
    if SupplierServices.objects.filter(user_id=user_id).exists():
            get_service_count=SupplierServices.objects.filter(user_id=user_id).count()
           
    return get_service_count
@register.filter(name='get_product_counter')
def get_product_counter(user_id):
    get_product_count = 0
    if SupplierProduct.objects.filter(user_id=user_id).exists():
            get_product_count=SupplierProduct.objects.filter(user_id=user_id).count()

    return get_product_count