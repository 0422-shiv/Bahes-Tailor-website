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
from admin_settings.models import System_settings
from django.template.loader import render_to_string, get_template
import smtplib
import email.message
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from manage_admin_settings.models import *



# @method_decorator(login_required, name="dispatch")
class Questions(generic.TemplateView):
	template_name = 'survey/supplier.html'

	def get(self, request, id, *args, **kwargs):
		get_system_settings = System_settings.objects.all()
		ques=request.GET['q']
		if 'type' in request.GET:
			UserProfile.objects.filter(id=id).update(user_type=get_object_or_404(UserType,type_name=request.GET['type']))
		user_instance = get_object_or_404(UserProfile, id=id)
	   

		current_ques=ques   # 1
		next_ques=int(ques)+1 # 2
		# next_next_ques = int(ques)+2
		show_submit = True
		get_questions = QuestionsTable.objects.filter(question_for__type_name=user_instance.user_type.type_name).filter(priority_type=current_ques)

		if QuestionsTable.objects.filter(question_for__type_name=user_instance.user_type.type_name).filter(priority_type=next_ques).exists():
			show_submit = False

		return render(request, self.template_name, {'get_system_settings':get_system_settings,'show_submit':show_submit,'get_questions': get_questions,'id':id,'current_ques':current_ques,'next_ques':next_ques})

	def post(self, request, id, *args, **kwargs):
		ques = request.GET['q']
		ques_in_int=int(ques)
	   
		ques_in_str=str(ques_in_int+1)
		que = request.POST['que']
		ans = request.POST['ans']
		id = str(id)
		if ans == "":
			return redirect(BASE_URL + 'survey/' + id+'?q='+ ques)
			
		else:
			ans = request.POST['ans']
			userprofile_instance = get_object_or_404(UserProfile, id=id)
			user_instance = get_object_or_404(User, id=userprofile_instance.user_id.id)
			question_instance=get_object_or_404(QuestionsTable,question=que)
			if UserAnswerTable.objects.filter(question=question_instance).filter(user=user_instance).exists():
				UserAnswerTable.objects.filter(question=question_instance).filter(user=user_instance).update(answer=ans)
			else:
				saveans=UserAnswerTable(user=user_instance,question=question_instance,answer=ans)
				saveans.save()

		   
			if 'next' in request.POST:
				return redirect(BASE_URL + 'survey/' + id+'?q='+ques_in_str)
			else:
				if not request.user.is_authenticated:
					username=user_instance.email
					password=userprofile_instance.passward
					if User.objects.filter(email=username).exists():
						login_url=BASE_URL+'account/login'
						data_content = {"username": userprofile_instance.full_name,"login_url":login_url,}
						email_content = 'email_template/registration.html'
						

						email_template = get_template(email_content).render(data_content)
						reciver_email = username

						Subject = userprofile_instance.full_name+' Has Been Registered, Congratulations!'

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
					
					
					# return HttpResponseRedirect(reverse('dashboard:EditProfile'))
					

						user = auth.authenticate(username=username, password=password)
						
						if user is not None:
								auth.login(request, user)
								# return HttpResponseRedirect(reverse('dashboard:EditProfile'))
								if request.user.userx.user_type.type_name == 'supplier':
									return redirect(BASE_URL+'dashboard/')
								else:
									return redirect(BASE_URL+'dashboard/profile/')
				else:
					if request.user.userx.user_type.type_name == 'supplier':
						return redirect(BASE_URL+'dashboard/')
					else:
						return redirect(BASE_URL+'dashboard/profile/')
