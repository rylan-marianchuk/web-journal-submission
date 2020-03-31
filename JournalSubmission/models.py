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
    inReview = models.BooleanField(default=False)
    editorApproved = models.BooleanField(default=False)
    feedbackReady = models.BooleanField(default=False)
    resubmissions_remaining = models.IntegerField(default=3)
    reviewer1 = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='reviewer_1',
                                  null= True, blank=True)

    reviewer2 = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='reviewer_2',
                                  null= True, blank=True)

    reviewer3 = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='reviewer_3',
                                  null = True, blank=True)

    reviewer1_FEED = models.CharField(max_length=5000, default="")
    reviewer2_FEED = models.CharField(max_length=5000, default="")
    reviewer3_FEED = models.CharField(max_length=5000, default="")

    file = models.FileField()

    # integers in this set indicate the reviewer that has made their decision
    seen_accept = models.CharField(max_length=6, default="")
    # ^ is a string in form : reviewer# bit bool accepted : eg 112030 means rev 1 accepted and 2 and 3 rejected

    def __str__(self):
        return self.title


    def reviewed(self, reviewer_number, accepted):
        """
        Update the seen accept string to the given reviewer number and whether they accepted or not
        :param reviewer_number: [1,3]
        :param accepted: bool
        :return:
        """

        if accepted:
            self.seen_accept += str(reviewer_number) + "1"
        else:
            self.seen_accept += str(reviewer_number) + "0"
        return


    def isReviewed(self):
        """
        :return: bool whether all reviewers have submitted their feedback for this submission
        """
        return len(self.seen_accept) == 6


    def didSee(self, reviewer_number):
        """
        Return a bool whether the specified reviewer did submit their feedback
        :param reviewer_number:
        :return: bool
        """
        for i in range(0, len(self.seen_accept), 2):
            if self.seen_accept[i] == str(reviewer_number):
                return True
        return False


    def didReject(self, reviewer_number):
        """
        Assume isReviewed is true, that is all reviewers have already provided feedback
        Return bool whether the given reviewer rejected this submission
        :param reviewer_number:
        :return:
        """
        for i in range(0, 5, 2):
            if self.seen_accept[i] == str(reviewer_number):
                return int(self.seen_accept[i+1]) == 0
