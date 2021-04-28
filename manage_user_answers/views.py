from django.shortcuts import render,get_object_or_404
from django.views import generic
from survey.models import *
from django.db.models import Q
import string
# Create your views here.
class SupplierAnswer(generic.TemplateView):
	template_name = 'admin/manage-user-answers/supplier-answers.html'
	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
			question=None
			option=None
			if 'question' in request.GET and 'option' in request.GET :
				question = request.GET['question']
				option = request.GET['option']
				get_question=QuestionsTable.objects.filter(question_for__type_name='supplier')
				get_answer=None
				for data in get_question:
					

					if ((data.question).translate({ord(c): None for c in string.whitespace})) == ((question).translate({ord(c): None for c in string.whitespace})):

						if option == 'A' or option == 'a':
							get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='supplier').filter(question__question=data.question).filter(answer__iexact=data.option_a)
						elif option == 'B' or option == 'b':
							get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='supplier').filter(question__question=data.question).filter(answer__iexact=data.option_b)
						elif option == 'C' or option == 'c':
							get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='supplier').filter(question__question=data.question).filter(answer__iexact=data.option_c)
						elif option == 'D' or option == 'd':
							get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='supplier').filter(question__question=data.question).filter(answer__iexact=data.option_d)
		
			else: 
				get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='supplier')
				get_question=QuestionsTable.objects.filter(question_for__type_name='supplier')
			return render(request, self.template_name,{'get_answer':get_answer,'get_question':get_question,'question':question,'option':option})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))
		


class CustomerAnswer(generic.TemplateView):
	template_name = 'admin/manage-user-answers/customer-answers.html'
	def get(self, request,*args, **kwargs):
		if request.user.is_superuser:
				question=None
				option=None
				if 'question' in request.GET and 'option' in request.GET :
					question = request.GET['question']
					option = request.GET['option']
					
					get_question=QuestionsTable.objects.filter(question_for__type_name='customer')
					get_answer=None
					for data in get_question:
						if ((data.question).translate({ord(c): None for c in string.whitespace})) == ((question).translate({ord(c): None for c in string.whitespace})):

							if option == 'A' or option == 'a':
								get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='customer').filter(question__question=data.question).filter(answer__iexact=data.option_a)
							elif option == 'B' or option == 'b':
								get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='customer').filter(question__question=data.question).filter(answer__iexact=data.option_b)
							elif option == 'C' or option == 'c':
								get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='customer').filter(question__question=data.question).filter(answer__iexact=data.option_c)
							elif option == 'D' or option == 'd':
								get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='customer').filter(question__question=data.question).filter(answer__iexact=data.option_d)
			
					
				
				else: 
					get_answer=UserAnswerTable.objects.filter(user__userx__user_type__type_name='customer').order_by('-id')
					get_question=QuestionsTable.objects.filter(question_for__type_name='customer')
				return render(request, self.template_name,{'get_answer':get_answer,'get_question':get_question,'question':question,'option':option})
		else:
			messages.error(request,"Please enter valid username and password")
			return HttpResponseRedirect(reverse('admin_login'))