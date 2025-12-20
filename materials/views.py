from django.shortcuts import render
from .models import Material
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from .forms import MaterialForm, MaterialUpdateForm

# Create your views here.

class MaterialListView(ListView):
    model = Material
    template_name = 'materials/materials.html'
    context_object_name = 'materials'
    
class MaterialCreateView(CreateView):
    model = Material
    template_name = 'materials/material_create.html'
    success_url = '/materials/'
    form_class = MaterialForm

class MaterialUpdateView(UpdateView):
    model = Material
    template_name = 'materials/material_update.html'
    success_url = '/materials/'
    form_class = MaterialUpdateForm

class MaterialDeleteView(DeleteView):
    model = Material    
    template_name = 'materials/material_confirm_delete.html'
    success_url = '/materials/'