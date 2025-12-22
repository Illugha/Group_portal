from django import forms
from .models import Theme, Posts

class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['topic', 'question', 'other_content', 'media']

class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['content', 'media', 'reaction']

class ThemeSortForm(forms.Form):
    topic = forms.CharField(required=False)


