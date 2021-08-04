from django.shortcuts import render,get_object_or_404
from django.views import generic
from survey.models import *
from django.db.models import Q
import string
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
class SupplierAnswer(generic.TemplateView):
	template_name = 'admin/manage-user-answers/supplier-answers.html'
	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			question=None
			option=None
			option_list=['A','B','C','D']
			correct_Option=None
			correct_answer=None
			
			if 'question' in request.GET and 'option' in request.GET :
				question = request.GET['question']
				option = request.GET['option']
				get_question=QuestionsTable.objects.filter(question_for__type_name='supplier')
				
				get_answer=None
				
				for data in get_question:
					

					if ((data.question).translate({ord(c): None for c in string.whitespace})) == ((question).translate({ord(c): None for c in string.whitespace})):
						if (data.answer).translate({ord(c): None for c in string.whitespace}) == (data.option_a).translate({ord(c): None for c in string.whitespace}):
							correct_Option='A'
							correct_answer=data.answer
						elif (data.answer).translate({ord(c): None for c in string.whitespace}) == (data.option_b).translate({ord(c): None for c in string.whitespace}):
							correct_Option='B'
							correct_answer=data.answer
						elif (data.answer).translate({ord(c): None for c in string.whitespace}) == (data.option_c).translate({ord(c): None for c in string.whitespace}):
							correct_Option='C'
							correct_answer=data.answer
						elif (data.answer).translate({ord(c): None for c in string.whitespace}) == (data.option_d).translate({ord(c): None for c in string.whitespace}):
							correct_Option='D'
							correct_answer=data.answer

						if option == 'A':
							get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='supplier').filter(question__question=data.question).filter(answer__iexact=data.option_a)
						elif option == 'B':
							get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='supplier').filter(question__question=data.question).filter(answer__iexact=data.option_b)
						elif option == 'C':
							get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='supplier').filter(question__question=data.question).filter(answer__iexact=data.option_c)
						elif option == 'D':
							get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='supplier').filter(question__question=data.question).filter(answer__iexact=data.option_d)
		
			else: 
				get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='supplier')
				get_question=QuestionsTable.objects.filter(question_for__type_name='supplier')

			return render(request, self.template_name,{'correct_Option':correct_Option,'correct_answer':correct_answer,'option_list':option_list,'get_answer':get_answer,'get_question':get_question,'question':question,'option':option})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
		


class CustomerAnswer(generic.TemplateView):
	template_name = 'admin/manage-user-answers/customer-answers.html'
	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
				question=None
				option=None
				option_list=['A','B','C','D']
				correct_Option=None
				correct_answer=None
				if 'question' in request.GET and 'option' in request.GET :
					question = request.GET['question']
					option = request.GET['option']
					
					get_question=QuestionsTable.objects.filter(question_for__type_name='customer')
					
					get_answer=None
					
					
					for data in get_question:
						if ((data.question).translate({ord(c): None for c in string.whitespace})) == ((question).translate({ord(c): None for c in string.whitespace})):
							if (data.answer).translate({ord(c): None for c in string.whitespace}) == (data.option_a).translate({ord(c): None for c in string.whitespace}):
								correct_Option='A'
								correct_answer=data.answer
							elif (data.answer).translate({ord(c): None for c in string.whitespace}) == (data.option_b).translate({ord(c): None for c in string.whitespace}):
								correct_Option='B'
								correct_answer=data.answer
							elif (data.answer).translate({ord(c): None for c in string.whitespace}) == (data.option_c).translate({ord(c): None for c in string.whitespace}):
								correct_Option='C'
								correct_answer=data.answer
							elif (data.answer).translate({ord(c): None for c in string.whitespace}) == (data.option_d).translate({ord(c): None for c in string.whitespace}):
								correct_Option='D'
								correct_answer=data.answer

							if option == 'A':
								get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='customer').filter(question__question=data.question).filter(answer__iexact=data.option_a)
							elif option == 'B':
								get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='customer').filter(question__question=data.question).filter(answer__iexact=data.option_b)
							elif option == 'C':
								get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='customer').filter(question__question=data.question).filter(answer__iexact=data.option_c)
							elif option == 'D':
								get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='customer').filter(question__question=data.question).filter(answer__iexact=data.option_d)
			
					
				
				else: 
					get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='customer').order_by('-id')
					get_question=QuestionsTable.objects.filter(question_for__type_name='customer')
					
					
				return render(request, self.template_name,{'option_list':option_list,'correct_Option':correct_Option,'correct_answer':correct_answer,'get_answer':get_answer,'get_question':get_question,'question':question,'option':option})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))