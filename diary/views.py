from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Grade
from .forms import GradeForm


class GradeListView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = 'diary/grade_list.html'
    context_object_name = 'grades'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Grade.objects.all()
        return Grade.objects.filter(student__user=self.request.user)


class GradeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'diary/grade_form.html'
    success_url = reverse_lazy('dairy:grade-list')

    def test_func(self):
        return self.request.user.profile.role in ['moderator', 'admin']
        #return self.request.user.is_staff


class GradeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'diary/grade_form.html'
    success_url = reverse_lazy('dairy:grade-list')

    def test_func(self):
        return self.request.user.profile.role in ['moderator', 'admin']
        #return self.request.user.is_staff


class GradeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Grade
    template_name = 'diary/grade_confirm_delete.html'
    success_url = reverse_lazy('dairy:grade-list')

    def test_func(self):
        return self.request.user.profile.role in ['moderator', 'admin']
        #return self.request.user.is_staff



        
