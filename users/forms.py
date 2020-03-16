from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
#from django.contrib.auth.models import forms
from .models import Profile
from django.db import models


USER_TYPES = [('author', 'Author'), ('editor', 'Editor'), ('reviewer', 'Reviewer')]


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileDetailsForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['institute', 'discipline', 'role']



class LoginForm(forms.ModelForm):
    userName = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['userName', 'password']
