from django.shortcuts import render, redirect
from .models import Theme, Posts
from django.views.generic import ListView,  DetailView, CreateView, View, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponseRedirect
from .forms import ThemeForm, PostsForm, ThemeSortForm
from django.urls import reverse
# Create your views here.

class ThemesListView(ListView):
    model = Theme
    template_name = 'forum/themes_list.html'
    context_object_name='themes'

    def get_queryset(self):
        queryset = super().get_queryset()
        topic = self.request.GET.get('topic', '')
        if topic:
            queryset = queryset.filter(topic=topic)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ThemeSortForm(self.request.GET)

        return context


class CreateTheme(CreateView):
    model = Theme
    template_name='forum/theme_creation.html'
    form_class = ThemeForm
    success_url = reverse_lazy("theme-list")
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ThemeDetailView(DetailView):
    model = Theme
    template_name = 'forum/theme_details.html'
    context_object_name = "theme"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Posts.objects.filter(theme=self.object)
        return context

class PostCreationView(CreateView):
    model = Posts
    template_name = "forum/post_create.html"
    form_class = PostsForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['theme'] = Theme.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.theme = Theme.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('theme-detail', kwargs={'pk': self.object.pk})
    

class ThemeDeletionView(DeleteView):
    model = Theme
    template_name = 'forum/delete_page.html'
    success_url = reverse_lazy('theme-list')

class ThemeUpdateView(UpdateView):
    model = Theme
    template_name = 'forum/update_page.html'
    form_class = ThemeForm
    success_url = reverse_lazy('theme-list')