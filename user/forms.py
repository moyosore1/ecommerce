from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
        	'username': forms.TextInput(attrs={'class':'form-control', 'required':True}), 
        	'email':forms.EmailInput(attrs={'class':'form-control', 'required':True}),
        	'password1':forms.PasswordInput(attrs={'class':'form-control', 'required':True}),
        	'password2':forms.PasswordInput(attrs={'class':'form-control', 'required':True}),

        }


