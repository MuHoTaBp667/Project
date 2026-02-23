from django import forms
from .models import PsAuths, PsAors, PsEndpoints

CONTEXT_CHOICES = [
    ('internal', 'Internal'),
    ('internal_only', 'Internal_only'),
]
# создаем выбор для поля context

class AddUserForm(forms.ModelForm):

    class Meta:
        model = PsEndpoints
        fields = (
             "id",
             "context",
             "callerid",
             "tnumber",
        )
        # берем поля из бд
        widgets = {
            'id':forms.TextInput(attrs={'placeholder': 'Введите ID'}),
            'callerid':forms.TextInput(attrs={'placeholder': 'Введите CallerID'}),
            'tnumber':forms.TextInput(attrs={'placeholder': 'Введите Tnumber'}),
            'context': forms.Select(attrs={'class': 'form-control'},
                                    choices=CONTEXT_CHOICES)
        }
        # настраиваем плейсхолдеры для текста

