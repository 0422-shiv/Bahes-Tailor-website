from django.contrib import admin

from .models import  QuestionsTable, UserAnswerTable


admin.site.register(QuestionsTable)
admin.site.register(UserAnswerTable)
