from django import forms
from .models import User, USER_TYPES




class UserForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    userType = forms.CharField(max_length=100, widget=forms.Select(choices=USER_TYPES))
    userName = forms.CharField(max_length=100)
    emailAddress = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    discipline = forms.CharField(max_length=100)
    instituition = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['name', 'userName', 'emailAddress', 'instituition', 'password', 'discipline', 'userType']


