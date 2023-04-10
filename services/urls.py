from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('questionnaire/<int:pk>', views.QuestionnaireDetail.as_view(), name='questionnaire_detail'),
    path('questionnairelist', views.QuestionnaireList.as_view(),name='questionnaire-list'),
    path('questionnaireremove/<int:pk>',views.QuestionnaireRemove.as_view(), name='questionnaire-remove'),
    path('questionnaireupdate/<int:pk>',views.QuestionnaireUpdate.as_view(), name='questionnaire-update'),
    path('questionnairecreate', views.QuestionnaireCreate.as_view(), name='questionnaire-create'),
    path('question/<int:pk>', views.QuestionDetail.as_view(), name='question-detail'),
    path('questionremove/<int:pk>', views.QuestionRemove.as_view(), name='question-remove'),
    path('questionupdate/<int:pk>', views.QuestionUpdate.as_view(), name='question-update'),
    path('questioncreate/<int:questionnaireid>', views.QuestionCreate.as_view(), name='question-create'),
    path('answercreate/<int:questionid>', views.AnswerCreate.as_view(), name='answer-create'),
    path('answerremove/<int:pk>', views.AnswerRemove.as_view(), name='answer-remove'),
    path('answerupdate/<int:pk>', views.AnswerUpdate.as_view(), name='answer-update'),
    path('gamecreate/<int:questionnaireid>', views.GameCreate.as_view(), name='game-create'),
    path('gameUpdateParticipant', views.UpdateParticipant.as_view(), name='game-updateparticipant'),
    path('gamecountdown', views.CountDown.as_view(), name='game-count-down'),
]
