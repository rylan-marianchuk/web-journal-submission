from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile



USER_TYPES = [('author', 'Author'), ('editor', 'Editor'), ('reviewer', 'Reviewer')]

'''By using a OneToOneField, one can indeed extend the user system, 
but you can not simply use this to handle both models in the same Form,
and thus construct two objects at once - Stackoverflow Answer'''

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileDetailsForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['institute', 'discipline', 'role']


