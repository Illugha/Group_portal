from django import forms
from .models import Poll, Question, Answer

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description']
        labels = {
            'title': 'Назва опитування',
            'description': 'Опис опитування',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        labels = {
            'question_text': 'Текст питання',
        }
        widgets = {
            'question_text': forms.TextInput(attrs={'class': 'form-control'}),
        }

Answers_set = forms.inlineformset_factory(
    Question,
    Answer,
    fields=['answer_text'],
    extra=4,
    can_delete=True,
    widgets={
        'answer_text': forms.TextInput(attrs={'class': 'form-control'}),
    }
)
