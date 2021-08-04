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
from datetime import datetime


@method_decorator(login_required(login_url='/account/login'), name="dispatch")
class EditProfile(generic.TemplateView):
    template_name = 'dashboard/profile.html'

    def get(self, request, *args, **kwargs):
        if 'tips' in request.GET:
            tips=request.GET['tips']
        else:
            tips=None
        if 'flag' in request.GET:
            if 'change_password' == request.GET['flag']:
                flag='change_password'
            else:
                flag='profile'
        else:
            flag='profile'
        get_system_settings = System_settings.objects.all()
        user_instance = get_object_or_404(User, id=request.user.id)
        get_countries=Countries.objects.all()
        form = MyPasswordChangeForm(request.user)
        if UserProfile.objects.filter(user_id=user_instance).exists():
            userprofile = get_object_or_404(UserProfile,user_id=user_instance)
        else:
            # userprofile = UserProfile(user_id=request.user, created_by=request.user)
            # userprofile.save()
            # messages.error(request, "profile info is not found.")
            return HttpResponseRedirect(reverse('account:UserType'))
        # messages.warning(request, 'profile')
        return render(request, self.template_name,
                      {'tips':tips,'flag':flag,'userprofile': userprofile,  'form': form,'get_system_settings':get_system_settings,'get_countries':get_countries})

    def post(self, request, *args, **kwargs):
        user_instance = get_object_or_404(User, id=request.user.id)
        if 'phone' and 'full_name' in request.POST:
            # messages.warning(request, 'profile')
            flag='profile'
            if UserProfile.objects.filter(user_id=user_instance).exists():
                phone = request.POST["phone"]
                country = request.POST["country"]
              
                get_country=get_object_or_404(Countries,id=country)

                # user_instance = get_object_or_404(UserProfile, id=id)

                if UserProfile.objects.filter(phone=phone).filter(~Q(user_id=user_instance)).exists():
                    messages.error(request, phone + ' Phone number already exists', )
                else:

                    userupdate = get_object_or_404(UserProfile, user_id=user_instance)
                    userupdate.full_name = request.POST["full_name"]
                    userupdate.phone = request.POST["phone"]
                    userupdate.country = get_country
                    userupdate.tel_code = request.POST["tel_code"]

                    userupdate.save()
                    messages.success(request, 'Profile Updated Successfully')
        elif 'old_password' in  request.POST:
            messages.warning(request, 'change_password')
            flag='change_password'
            form = MyPasswordChangeForm(request.user, request.POST)

            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')

            else:
                messages.error(request, 'Please correct the error below.')
      
        else:
            flag='profile'
            messages.error(request, 'Something going wrong ,please try again')

      
        return redirect(BASE_URL+'dashboard/profile/?flag='+flag)
     
@login_required
def ProfileChange(request):
    if request.method == 'POST':
        
        user_instance = get_object_or_404(User, id=request.user.id)
        
        if 'save_profile_image' in request.POST:
          
            userupdate = get_object_or_404(UserProfile,user_id=user_instance)
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
        if request.POST['pagename'] == 'profile':
             return HttpResponseRedirect(reverse('dashboard:EditProfile'))
        elif request.POST['pagename'] == 'chat':
            return redirect(BASE_URL+"chat/?chatbahesroom=chatbahesroom")
        elif request.POST['pagename'] == 'service':
            return HttpResponseRedirect(reverse('services:Services'))
        elif request.POST['pagename'] == 'product':
            return HttpResponseRedirect(reverse('products:product'))



@login_required
def OnlineStatus(request):
   
        if request.method == 'POST': 
            onlinestatus = request.POST["onlinestatus"]
            userid = request.POST["userid"]
            if onlinestatus == "True":
                status = False
            else:
                status = True
            if UserProfile.objects.filter(id=userid).exists():
               
                UserProfile.objects.filter(id=userid).update(online_status=status)
            return JsonResponse({'message': 'Status Changed successfully.'})
        # return HttpResponseRedirect(reverse('dashboard:EditProfile'))



@register.filter(name='get_paid_status')
def get_paid_status(user):
    get_paid_status = False
    if BahesPayment.objects.filter(user_id=user.user_id).exists():
            get_user_ins=get_object_or_404(BahesPayment,user_id=user.user_id)
            get_paid_status=get_user_ins.payment_status
              
    return get_paid_status