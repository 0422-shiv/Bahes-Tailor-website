from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from account.models import UserType


class QuestionsTable(models.Model):

    question = models.CharField(max_length=100, null=True)
    option_a = models.CharField(max_length=100, null=True)
    option_b = models.CharField(max_length=100, null=True)
    option_c = models.CharField(max_length=100, null=True)
    option_d = models.CharField(max_length=100, null=True)
    answer = models.CharField(max_length=100, null=True )
    question_for = models.ForeignKey(UserType,related_name='question_for', on_delete=models.CASCADE, null=True)
    priority_type = models.IntegerField(null=True)
    status=models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name='question_created_by', on_delete=models.CASCADE)


    def __str__(self):
        return str(self.question)

class UserAnswerTable(models.Model):

    user = models.ForeignKey(User,related_name='answer_by_user', null=True, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionsTable,  on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.user)