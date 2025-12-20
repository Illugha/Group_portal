from django import forms
from .models import Mediafiles

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Mediafiles
        fields = ['title', 'description', 'media_file'] 