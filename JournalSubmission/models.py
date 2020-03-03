from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Journal(models.Model):
    # Each instance is a entry in the database
    # Fields in database
    title = models.CharField(max_length=100)

    # If an editor gets deleted, its journal will also be removed (on delete argument)
    editor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title