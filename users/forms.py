from django import forms
from .models import User, USER_TYPES




class UserForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    user_Type = forms.CharField(max_length=100, widget=forms.Select(choices=USER_TYPES))
    userName = forms.CharField(max_length=100)
    email_Address = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    discipline = forms.CharField(max_length=100)
    instituition = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['name', 'userName', 'email_Address', 'instituition', 'password', 'discipline', 'user_Type']

class LoginForm(forms.ModelForm):
    userName = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['userName', 'password']
