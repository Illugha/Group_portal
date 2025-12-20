from django.urls import path
from .views import PollView, PollCreateView, QuestionCreateView, AnswerCreateView

app_name = 'polls'

urlpatterns = [
    path('', PollView.as_view(), name='poll-list'),
    path('create/', PollCreateView.as_view(), name='poll-create'),
    path('create/question/<int:poll_id>/', QuestionCreateView.as_view(), name='question-create'),
    path('create/answer/<int:question_id>/<int:poll_id>', AnswerCreateView.as_view(), name='answer-create'),
]
