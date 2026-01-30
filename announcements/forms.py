from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):

    photo = forms.ImageField(label='Фото', required=False)
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'photo']

    
