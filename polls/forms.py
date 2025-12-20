from django import forms
from .models import Poll, Question, Answer

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

Answers_set = forms.inlineformset_factory(
    Question, Answer, fields=['answer_text'], extra=4, can_delete=True, widgets={
        'answer_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter answer text'}),
    })