from django.shortcuts import render, redirect
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

class AnswerCreateView(View):
    template_name = 'polls/answer_form.html'

    def get(self, request, question_id, poll_id):
        question = Question.objects.get(id=question_id)
        poll = Poll.objects.get(id=poll_id)
        formset = Answers_set(instance=question)
        return render(request, self.template_name, {
            'answers': formset,
            'question': question,
            'poll': poll,
        })

    def post(self, request, question_id, poll_id):
        question = Question.objects.get(id=question_id)
        poll = Poll.objects.get(id=poll_id)
        formset = Answers_set(request.POST, instance=question)

        if formset.is_valid():
            formset.save()  # Зберігаємо всі відповіді
            return redirect('polls:poll-list')  # Перекидання на список опитувань

        # Якщо є помилки — показуємо знову з помилками
        return render(request, self.template_name, {
            'answers': formset,
            'question': question,
            'poll': poll,
        })

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