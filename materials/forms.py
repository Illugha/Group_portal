from django import forms
from .models import Material
from django.forms import ModelForm
class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'description', 'image', 'video']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-image'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control-video'}),
        }

class MaterialUpdateForm(ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'description', 'image', 'video']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-image'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control-video'}),
        }