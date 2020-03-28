from django.db import models
from users.forms import Profile
from django.contrib.auth import get_user_model as user_model

# Create your models here.
class Journal(models.Model):
    # Each instance is a entry in the database
    # Fields in database
    title = models.CharField(max_length=1000)

    SUBJECTS = [('health & medicine', 'Health & Medicine'), ('humanities', 'Humanities'),
                ('mathematical sciences', 'Mathematical Science'), ('social sciences', 'Social Sciences'),
                ('physics', 'Physics'), ('computation', 'Computation')
            ]
    subject = models.CharField(max_length=200, choices=SUBJECTS, default='Humanities')


    # If an editor gets deleted, its journal will also be removed (on delete argument)
    editor = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.title


class Submission(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author')
    rejected = models.BooleanField(default=False)
    inReview = models.BooleanField(default=True)
    resubmissions_remaining = models.IntegerField(default=3)
    reviewer1 = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='reviewer_1')
    reviewer2 = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='reviewer_2')
    reviewer3 = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='reviewer_3')
    file = models.FileField()

    def __str__(self):
        return self.title
