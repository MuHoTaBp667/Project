from django import forms

class RegistrationForm(forms.Form):
    ID = forms.CharField(
        max_length=40, 
        label='ID',
        widget=forms.TextInput(attrs={'placeholder': 'Введите ID'})
    )
    CallerID = forms.CharField(
        max_length=40, 
        label='CallerID',
        widget=forms.TextInput(attrs={'placeholder': 'Введите CallerID'})
    )
    Tnumber = forms.CharField(
        max_length=40, 
        label='Tnumber',
        widget=forms.TextInput(attrs={'placeholder': 'Введите Tnumber'})
    )
    ContextRF = forms.ChoiceField(
        choices=[('internal', 'Internal'), ('internal_only', 'Internal_only')],
        widget=forms.Select(attrs={'placeholder': 'Выберите контекст'}),
        label='Context'
    )