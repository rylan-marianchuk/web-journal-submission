from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, forms
# Create your models here.
USER_TYPES = [('Author', 'Author'), ('Editor', 'Editor'), ('Reviewer', 'Reviewer')]

class User(models.Model):
    name = models.CharField(max_length=100)
    userName = models.CharField(max_length=100)
    email_Address = models.CharField(max_length=100)
    instituition = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    discipline = models.CharField(max_length=100)
    hasNotification = False
    user_Type = models.CharField(max_length=100, choices=USER_TYPES)



    def __str__(self):
        return self.userName

    def get_absolute_url(self):
        return "/profile/%i/" % self.userName



