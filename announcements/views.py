from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Announcement
from .forms import AnnouncementForm
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView


class AnnouncementListView(ListView):
    model = Announcement
    template_name = "announcements/announcement_list.html"
    context_object_name = "announcements"

class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = "announcements/announcement_detail.html"
    context_object_name = "announcement"

class AnnouncementCreateView(CreateView):
    model = Announcement
    template_name = "announcements/announcement_create.html"
    form_class = AnnouncementForm  
    success_url = reverse_lazy('announcements:announcement-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class AnnouncementUpdateView(UpdateView):
    model = Announcement
    template_name = "announcements/announcement_update.html"
    form_class = AnnouncementForm
    success_url = reverse_lazy('announcements:announcement-list')


class AnnouncementDeleteView(DeleteView):
    model = Announcement
    template_name = "announcements/announcement_delete.html"
    success_url = reverse_lazy('announcements:announcement-list')
