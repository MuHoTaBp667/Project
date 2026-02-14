from django import forms
from django.shortcuts import render, redirect

class RegistrationForm(forms.Form):
    ID = forms.CharField(max_length=40, label='ID')
    CallerID = forms.CharField(max_length=40, label='CallerID')
    Tnumber = forms.CharField(max_length=40, label='Tnumber')
    ContextRF = forms.ChoiceField (
        choices=[('internal', 'Intertnal'),('internal_only', 'Internal_only')],
        widget=forms.Select,
        label='Context'
    )
    
