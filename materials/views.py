from django.shortcuts import render
from .models import Material
from django.views.generic import CreateView, DeleteView, UpdateView, ListView

# Create your views here.

class MaterialListView(ListView):
    model = Material
    template_name = 'materials/materials.html'
    context_object_name = 'materials'
    
class MaterialCreateView(CreateView):
    model = Material
    fields = ['name', 'description', 'image', 'video']
    template_name = 'materials/material_create.html'
    success_url = '/materials/'

class MaterialUpdateView(UpdateView):
    model = Material
    fields = ['name', 'description', 'image', 'video']
    template_name = 'materials/material_update.html'
    success_url = '/materials/'

class MaterialDeleteView(DeleteView):
    model = Material
    template_name = 'materials/material_confirm_delete.html'
    success_url = '/materials/'