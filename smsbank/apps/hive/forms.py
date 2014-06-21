# coding: utf-8
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SMSForm(forms.Form):
    """Send SMS from device form"""
    phone = forms.RegexField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        regex=r'^\+?1?\d{9,15}$',
        error_message=(u'Указан неправильный номер')
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )


class CustomAuthForm(AuthenticationForm):
    """Custom login form"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class CustomRegisterForm(UserCreationForm):
    """Custom registration form"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
