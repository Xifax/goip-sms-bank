# coding: utf-8
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from smsbank.apps.hive.models import CallForwarding


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


class CallForwardingForm(forms.ModelForm):
    """Call forwarding profile fields"""
    login = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': u'Логин'
        }),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': u'Пароль'
        }),
        required=True
    )

    FORWARDING_METHODS = (
        ('pstn', 'PSTN'),
        ('local', 'Local SIP'),
        ('remote', 'Remote SIP')
    )
    forwarding = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=FORWARDING_METHODS,
        required=False
    )

    host = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': u'Сервер'
        }),
        required=False
    )
    port = forms.RegexField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': u'Порт'
        }),
        regex=r'^\d+$',
        required=False
    )

    PROTOCOLS = (
        (True, 'UDP'),
        (False, 'TCP')
    )
    protocol = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=PROTOCOLS,
        required=False
    )

    def clean_port(self):
        """Cast empty port to 0"""
        port = self.cleaned_data['port']
        if not port:
            port = 0
        return port

    class Meta:
        """Associate with call forwarding profile"""
        model = CallForwarding
        exclude = ('user',)
