# Import some useful packages.
from django.urls import path

from . import views

# Define urls for User Application function.
urlpatterns = [
path('', views.ManageQuestions.as_view(), name="ManageQuestions"),
path('edit-question/<int:id>', views.EditQuestion.as_view(), name="EditQuestion"),
path('questionstatus', views.QuestionStatus.as_view(), name="QuestionStatus"),
]