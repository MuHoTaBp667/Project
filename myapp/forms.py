from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import PsAuths, PsAors, PsEndpoints
import re

CONTEXT_CHOICES = [
    ('internal', 'Internal'),
    ('internal_only', 'Internal_only'),
]

def validate_digits_only(value):
    """Проверяет, что строка состоит только из цифр"""
    if not re.match(r'^\d+$', value):
        raise ValidationError('Поле должно содержать только цифры')

class AddUserForm(forms.ModelForm):
    id = forms.CharField(
        max_length=4,
        min_length=4,
        validators=[
            RegexValidator(
                regex=r'^\d{4}$',
                message='ID должен содержать ровно 4 цифры',
                code='invalid_id'
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Введите ID (4 цифры)', 'id': 'id_field'})
    )
    
    callerid = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Автоматически из ID', 'id': 'callerid_field'}),
        help_text='Если оставить пустым - подставится <ID>'
    )
    
    tnumber = forms.CharField(
        max_length=5,
        min_length=5,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\d{5}$',
                message='TNumber должен содержать ровно 5 цифр',
                code='invalid_tnumber'
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Введите Tnumber (5 цифр)'})
    )
    
    class Meta:
        model = PsEndpoints
        fields = (
            "id",
            "context",
            "callerid",
            "tnumber",
        )
        widgets = {
            'context': forms.Select(attrs={'class': 'form-control'}, choices=CONTEXT_CHOICES)
        }
    
    def clean_callerid(self):
        """Если callerid не заполнен, подставляем <id>"""
        callerid = self.cleaned_data.get('callerid')
        user_id = self.cleaned_data.get('id')
        
        if not callerid or callerid.strip() == '':
            if user_id:
                return f'<{user_id}>'
        return callerid
    
    def clean_id(self):
        id_value = self.cleaned_data.get('id')
        
        if not self.instance.pk and PsEndpoints.objects.filter(id=id_value).exists():
            raise ValidationError('Пользователь с таким ID уже существует')
        
        return id_value

