from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views import generic
from django.db.models import Q
from account.models import *
from findsupplier.models import *
from survey.models import *
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from bahes.settings import BASE_URL
from django.template.defaulttags import register
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name="dispatch")
class ManageQuestions(generic.TemplateView):
	template_name = 'admin/manage-questions/manage-questions.html'


	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:

			get_supplier_questions=QuestionsTable.objects.filter(question_for__type_name='supplier').order_by('-id')
			get_customer_questions=QuestionsTable.objects.filter(question_for__type_name='customer').order_by('-id')
			return render(request, self.template_name,{'get_supplier_questions':get_supplier_questions,'get_customer_questions':get_customer_questions})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
		

@method_decorator(login_required, name="dispatch")
class EditQuestion(generic.TemplateView):
	template_name = 'admin/manage-questions/edit-question.html'


	def get(self, request,*args,id, **kwargs):
		if request.user.is_superuser:

			get_question_instance=get_object_or_404(QuestionsTable,id=id)
			return render(request, self.template_name,{'get_question_instance':get_question_instance})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))


	def post(self, request, *args,id, **kwargs):
		if request.user.is_superuser:
			question=request.POST['question']
			option_a=request.POST['option_a']
			option_b=request.POST['option_b']
			option_c=request.POST['option_c']
			option_d=request.POST['option_d']
			if QuestionsTable.objects.filter(id=id).exists():
			   
				QuestionsTable.objects.filter(id=id).update(question=question,option_a=option_a,option_b=option_b,option_c=option_c,option_d=option_d)
				messages.success(request,"successfully Updated")
			return HttpResponseRedirect(reverse('manage_questions:ManageQuestions'))
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))

@method_decorator(login_required, name="dispatch")
class QuestionStatus(generic.TemplateView):
	template_name = 'admin/manage-questions/manage-questions.html'


	def post(self, request, *args, **kwargs):
		if request.user.is_superuser:

			questionid = request.POST["questionid"]
			questionstatus = request.POST["questionstatus"]

			if questionstatus == "True":
				status = False
			else:
				status = True
			if QuestionsTable.objects.filter(id=questionid).exists():
			   
				QuestionsTable.objects.filter(id=questionid).update(status=status)
			return JsonResponse({'message': 'Status Changed successfully.'})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
