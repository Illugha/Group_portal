from django import forms
from django.forms import inlineformset_factory
from .models import Vote, VoteOption, VoteResponse


class VoteForm(forms.ModelForm):
    """Форма для створення/редагування голосування"""
    
    class Meta:
        model = Vote
        fields = [
            'title', 
            'description', 
            'is_active', 
            'start_date', 
            'end_date', 
            'allow_revote',
            'is_anonymous'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть назву голосування'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Опис голосування'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'allow_revote': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_anonymous': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'title': 'Назва голосування',
            'description': 'Опис',
            'is_active': 'Активне',
            'start_date': 'Дата початку',
            'end_date': 'Дата завершення',
            'allow_revote': 'Дозволити переголосування',
            'is_anonymous': 'Анонімне голосування'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if end_date <= start_date:
                raise forms.ValidationError(
                    "Дата завершення має бути пізніше дати початку"
                )
        
        return cleaned_data


class VoteOptionForm(forms.ModelForm):
    """Форма для варіанту відповіді"""
    
    class Meta:
        model = VoteOption
        fields = ['text', 'order']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Варіант відповіді'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            })
        }
        labels = {
            'text': 'Варіант відповіді',
            'order': 'Порядок'
        }


# Formset для варіантів голосування
VoteOptionFormSet = inlineformset_factory(
    Vote,
    VoteOption,
    form=VoteOptionForm,
    extra=3,  # Кількість пустих форм
    min_num=2,  # Мінімум 2 варіанти
    validate_min=True,
    can_delete=True
)


class VoteResponseForm(forms.Form):
    """Форма для голосування користувача"""
    vote_option = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label="Оберіть варіант",
        empty_label=None
    )
    
    def __init__(self, *args, **kwargs):
        vote = kwargs.pop('vote', None)
        super().__init__(*args, **kwargs)
        
        if vote:
            self.fields['vote_option'].queryset = vote.options.all()
            # Налаштовуємо відображення варіантів
            self.fields['vote_option'].label_from_instance = lambda obj: obj.text


class VoteSearchForm(forms.Form):
    """Форма пошуку голосувань"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пошук голосувань...'
        }),
        label='Пошук'
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Всі'),
            ('active', 'Активні'),
            ('closed', 'Завершені'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Статус'
    )
    
    voted = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Всі'),
            ('yes', 'Проголосовано'),
            ('no', 'Не проголосовано'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Мій статус'
    )