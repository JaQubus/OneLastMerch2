from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


# basic Django register form
class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    pass
