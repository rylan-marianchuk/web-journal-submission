from django.db import models
from django.contrib.auth.models import User

USER_TYPES = [('author', 'Author'), ('editor', 'Editor'), ('reviewer', 'Reviewer')]


'''User Model is extended with Profile based on  OneToOneField method/relationship, to add in other required
fields like role, discipline and institute  which User Model does not offer by default'''

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=USER_TYPES, default='Author')
    discipline = models.CharField(max_length=100, blank=True)
    institute = models.CharField(max_length=100, blank=True)

