from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Modify the UserCreationForm by creating a new class that inherit it.
class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta: # needs to be named Meta
        model = User # change the user model whenever we save something
        fields = ["username", "email", "password1", "password2"] # Set where the emailfield is located. All, except the email field is built in Django




