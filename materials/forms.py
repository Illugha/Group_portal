from django import forms
from .models import Material
from django.forms import ModelForm
class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'description', 'image', 'video', 'url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-image'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control-video'}),
            'url': forms.URLInput(attrs={'class': 'form-control-url'}),
        }

class MaterialUpdateForm(ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'description', 'image', 'video', 'url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-image'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control-video'}),
            'url': forms.URLInput(attrs={'class': 'form-control-url'}),
        }