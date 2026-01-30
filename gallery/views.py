from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Mediafiles
from .forms import GalleryForm


class GalleryListView(ListView):
    model = Mediafiles
    template_name = 'gallery/list.html'
    paginate_by = 9  
    context_object_name = 'galleries'
    
    def get_queryset(self):
        queryset = Mediafiles.objects.filter(status='approved')
        
        # Фильтрация по типу файла
        media_type = self.request.GET.get('type')
        if media_type in ['photo', 'video', 'audio']:
            queryset = queryset.filter(media_type=media_type)
        
        return queryset.order_by('-created_at')


class GalleryCreateView(LoginRequiredMixin, CreateView):
    model = Mediafiles
    form_class = GalleryForm
    template_name = 'gallery/add.html'
    success_url = reverse_lazy('gallery_list')  
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('gallery_list') 
    else:
        form = UserCreationForm()
    
    return render(request, 'gallery/reg.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('gallery_list')
    else:
        form = AuthenticationForm()
    
    return render(request, 'gallery/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('gallery_list')