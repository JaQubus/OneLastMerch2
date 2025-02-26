from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import CustomUser

# basic Django register form
class RegisterForm(UserCreationForm):
    # email = forms.EmailField()

    # class Meta:
    #     model = CustomUser
    #     fields = ["username", "email", "password1", "password2"]
    pass

class LoginForm(AuthenticationForm):
    pass
