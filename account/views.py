from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from datetime import datetime
from django.template.defaulttags import register
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q
import base64
from django.core.files.base import ContentFile
from django.contrib.auth import update_session_auth_hash
from django.utils.html import format_html
from account.forms import MyPasswordChangeForm
from bahes.settings import BASE_URL
from django.template.loader import render_to_string, get_template
import smtplib
import email.message
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from bahes import settings
from .forms import UserForm, UserProfileForm
from .models import *
import random as r
from admin_settings.models import System_settings
from django.contrib.auth import logout
from manage_admin_settings.models import *

class CreateUserView(generic.TemplateView):
    template_name = "account/registration.html"
    form1 = UserForm
    form2 = UserProfileForm
    get_system_settings = System_settings.objects.all()
    get_country=Countries.objects.all()
    def get(self, request, *args, **kwargs):
        usertype = request.GET['type']
        form1 = UserForm()
        form2 = UserProfileForm()

        return render(request, "account/registration.html", {'get_country':self.get_country,'form1': form1, 'form2': form2, 'usertype': usertype,'get_system_settings':self.get_system_settings})

    def post(self, request, *args, **kwargs):
        usertype = request.POST['usertype']
        form1 = self.form1(request.POST)
        form2 = self.form2(request.POST)
        password = request.POST['password1']
        usern = request.POST['username']
        usern=usern.lower()
        if not User.objects.filter(username=usern).exists():
        
            if form1.is_valid():
                if form2.is_valid():
                        get_usertype_obj = get_object_or_404(UserType, type_name=usertype)

                        saveuser = form1.save(commit=False)
                        
                        saveuser.username = (saveuser.username).lower()
                        saveuser.email = (saveuser.username).lower()
                    # saveuser.email = email
                        saveuser.save()
                        saveprofile = form2.save(commit=False)
                        num = ""
                        for c in request.POST['tel_code']:
                            if c.isdigit():
                                num = num + c
                        saveprofile.tel_code = num
                        saveprofile.user_id = saveuser
                        saveprofile.passward=password
                        saveprofile.user_type = get_usertype_obj
                        saveprofile.created_by = saveuser
                        saveprofile.save()

                        id = str(saveprofile.id)
                        return redirect(BASE_URL + 'account/verify/' + id)

        # else:
        #         messages.error(request, form2.errors)
        else:
            messages.error(request, "Can not be registered,Check Email")
        return render(request, "account/registration.html", {'get_country':self.get_country,'form1': form1, 'form2': form2, 'usertype': usertype,'get_system_settings':self.get_system_settings})


class UserTypes(generic.TemplateView):
    template_name = "account/customer.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not UserProfile.objects.filter(user_id=request.user).exists():
                userprofile_obj=UserProfile(user_id=request.user,full_name=(request.user.first_name)+' '+(request.user.last_name),verify_status=True,created_by=request.user)
                userprofile_obj.save()
        print(BASE_URL)
        get_usertypes = UserType.objects.all()
        get_system_settings = System_settings.objects.all()
        return render(request, self.template_name, {'get_usertypes': get_usertypes,'get_system_settings':get_system_settings,'BASE_URL':BASE_URL})


class OtpViewPage(generic.TemplateView):
    template_name = "account/otp.html"
    get_system_settings = System_settings.objects.all()
    def get(self, request, id, *args, **kwargs):
        otp=""
        for i in range(4):
            otp+=str(r.randint(1,9))
       

        userprofile_instance=get_object_or_404(UserProfile,id=id)
        userprofile_instance.otp=otp
        userprofile_instance.save()
        if User.objects.filter(email=userprofile_instance.user_id.email).exists():
            user = get_object_or_404(User, email=userprofile_instance.user_id.email)

            data_content = {"username": userprofile_instance.full_name,
                            "user_otp": userprofile_instance.otp}
            email_content = 'email_template/email.html'

            email_template = get_template(email_content).render(data_content)
            reciver_email = user.email

            Subject = 'Please Verify Your Email Address'
            if Email_Setting.objects.filter(status=True).exists():
                email_data = Email_Setting.objects.filter(status=True)
                for data in email_data:
                    EMAIL_HOST = data.smtp_host
                    EMAIL_PORT = data.smtp_port
                    EMAIL_HOST_USER = data.smtp_username
                    EMAIL_HOST_PASSWORD = data.smtp_password
            email_msg = EmailMessage(Subject, email_template, EMAIL_HOST_USER, [reciver_email],
                                     reply_to=[EMAIL_HOST_USER])
            email_msg.content_subtype = 'html'
            email_msg.send(fail_silently=False)
            id = str(id)
            messages.success(request, "Four digit code has been sent to your registered email "+userprofile_instance.user_id.email+"")
        else:
            messages.error(request, "Something going wrong")
        return render(request, self.template_name,{'id':id,'get_system_settings':self.get_system_settings})

    def post(self, request,id,  *args, **kwargs):
        id = str(id)
        otp = request.POST['otp']
  
        userprofile_instance = get_object_or_404(UserProfile, id=id)
        if userprofile_instance.otp == otp:
            userprofile_instance.verify_status = True
            userprofile_instance.save()
            # if User.objects.filter(email=userprofile_instance.user_id.email).exists():
            #         login_url=BASE_URL+'account/login'
            #         data_content = {"username": userprofile_instance.full_name,"login_url":login_url,}
            #         email_content = 'email_template/registration.html'
                    

            #         email_template = get_template(email_content).render(data_content)
            #         reciver_email = 'shiveshbhardwaj149@gmail.com'

            #         Subject = userprofile_instance.full_name+' Has Been Registered, Congratulations!'

            #         if Email_Setting.objects.filter(status=True).exists():
            #             email_data = Email_Setting.objects.filter(status=True)
            #             for data in email_data:
            #                 EMAIL_HOST = data.smtp_host
            #                 EMAIL_PORT = data.smtp_port
            #                 EMAIL_HOST_USER = data.smtp_username
            #                 EMAIL_HOST_PASSWORD = data.smtp_password
            #         email_msg = EmailMessage(Subject, email_template, EMAIL_HOST_USER, [reciver_email],
            #                                  reply_to=[EMAIL_HOST_USER])
            #         email_msg.content_subtype = 'html'
            #         email_msg.send(fail_silently=False)
                  
            messages.success(request, 'Your account successfully verified')
            return redirect(BASE_URL + 'survey/' + id+'?q=1')
        else:
            messages.error(request, 'Entered otp is wrong ,please enter again')
            return render(request, self.template_name, {'id': id})



class login_user(generic.TemplateView):
    template_name = "account/login.html"

    def get(self, request, *args, **kwargs):
        get_system_settings = System_settings.objects.all()
        return render(request, self.template_name,{'get_system_settings':get_system_settings})

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            email = (request.POST["email"]).lower()
            password = request.POST["password"]

            if User.objects.filter(email=email).exists():
                user_instance=get_object_or_404(User, email=email)
                userprofile_instance=get_object_or_404(UserProfile,user_id=user_instance)

                if userprofile_instance.verify_status == True:
                    user = auth.authenticate(username=email, password=password)
                    if user is not None:
                        auth.login(request, user)
                        if request.user.userx.user_type.type_name == 'supplier':
                            return redirect(BASE_URL+'dashboard/')
                        else:
                            return redirect(BASE_URL+'dashboard/profile/')
                    else:
                        messages.error(request, 'Entered email or password was wrong ')
                else:
                    id=str(userprofile_instance.id)
                    message = format_html('your account is not activate <a href="{}">click here</a> to activate', ('verify/'+ id))
                    messages.error(request, message)
            else:
                messages.error(request, 'user is not registered')

            return redirect(BASE_URL+'account/login')


class ForgotPassword(generic.TemplateView):
    template_name = "account/forgot-password.html"
   
    def get(self, request, *args, **kwargs):
       

        return render(request, self.template_name)

class ForgotPasswordOtp(generic.TemplateView):
    template_name = "account/forgot-password-otp.html"

    def get(self, request,email, *args, **kwargs):
        email=email.lower()
        if User.objects.filter(email=email).exists():
            otp=""
            for i in range(4):
                otp+=str(r.randint(1,9))
            user = get_object_or_404(User, email=email)
            userprofile_instance=get_object_or_404(UserProfile,user_id=user)
            userprofile_instance.otp=otp
            userprofile_instance.save()
            data_content = {"username": userprofile_instance.full_name,
                            "user_otp": userprofile_instance.otp}
            email_content = 'email_template/otp.html'

            email_template = get_template(email_content).render(data_content)
            reciver_email = user.email

            Subject = 'Need a password?'
            if Email_Setting.objects.filter(status=True).exists():
                email_data = Email_Setting.objects.filter(status=True)
                for data in email_data:
                    EMAIL_HOST = data.smtp_host
                    EMAIL_PORT = data.smtp_port
                    EMAIL_HOST_USER = data.smtp_username
                    EMAIL_HOST_PASSWORD = data.smtp_password
            email_msg = EmailMessage(Subject, email_template, EMAIL_HOST_USER, [reciver_email],
                                     reply_to=[EMAIL_HOST_USER])
            email_msg.content_subtype = 'html'
            email_msg.send(fail_silently=False)
            
            messages.success(request, "OTP has been sent to your registered email if not then resend again")
            return render(request, self.template_name,{'email':email})
        else:
            messages.error(request, "please enter registered email")
            return HttpResponse("False")
        

        

class PasswordReset(generic.TemplateView):
    template_name = "account/password-reset.html"

    def get(self, request,otp,email ,*args, **kwargs):
        email=email.lower()
        user = get_object_or_404(User, email=email)
        userprofile_instance=get_object_or_404(UserProfile,user_id=user)
        if userprofile_instance.otp == otp:
            # return JsonResponse({'status': 'True'})
            return render(request, self.template_name,{'email':email})
        else:
            return HttpResponse("False")


class NewPasswordDone(generic.TemplateView):
    def post(self, request, *args, **kwargs):
      
            password1 = request.POST["pw1"]
            password2 = request.POST["pw2"]
            email = (request.POST["email"]).lower()
            
            if password1 == password2:
                user_instance=get_object_or_404(User, email=email)
                user_instance.set_password(password1)
                user_instance.save()
            messages.success(request, "Password successfully Changed")
  
            return JsonResponse({'messages': 'Password successfully Changed'})
            

def logout_request(request):
    logout(request)
    
    return redirect(BASE_URL+'account/login')