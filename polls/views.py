from django.shortcuts import render
from .models import Poll, Question, Answer
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import Answers_set

# Create your views here.

class PollView(ListView):
    template_name = 'polls/poll_list.html'
    model = Poll
    context_object_name = 'polls'

class PollCreateView(CreateView):
    template_name = 'polls/poll_form.html'
    model = Poll
    fields = ['title', 'description', ]

    def get_success_url(self):
        return reverse_lazy('polls:question-create', kwargs={'poll_id': self.object.id})

class QuestionCreateView(CreateView):
    template_name = 'polls/question_form.html'
    model = Question
    fields = ['question_text']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll_id = self.kwargs['poll_id']
        context['poll'] = Poll.objects.get(id=poll_id)
        return context

    def form_valid(self, form):
        poll_id = self.kwargs['poll_id']
        form.instance.poll = Poll.objects.get(id=poll_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('polls:answer-create', kwargs={'question_id': self.object.id, 'poll_id': self.object.poll.id})

class AnswerCreateView(CreateView):
    template_name = 'polls/answer_form.html'
    model = Answer
    form_class = Answers_set

    def form_valid(self, form):
        question_id = self.kwargs['question_id']
        form.instance.question = Question.objects.get(id=question_id)
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_id = self.kwargs['question_id']
        poll_id = self.kwargs['poll_id']
        context['poll'] = Poll.objects.get(id=poll_id)
        context['question'] = Question.objects.get(id=question_id)
        if self.request.POST:
            context['answers'] = Answers_set(self.request.POST, instance=context['question'])
        else:
            context['answers'] = Answers_set(instance=context['question'])
        return context

    def get_success_url(self):
        return reverse_lazy('polls:poll-list')

class PollDetailView(DetailView):
    template_name = 'polls/poll_detail.html'
    model = Poll
    context_object_name = 'poll'

class PollUpdateView(UpdateView):
    template_name = 'polls/poll_form.html'
    model = Poll
    fields = ['title', 'description', ]
    success_url = '/polls/'

class PollDeleteView(DeleteView):
    template_name = 'polls/poll_confirm_delete.html'
    model = Poll
    success_url = '/polls/'