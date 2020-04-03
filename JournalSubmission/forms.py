from django.forms import ModelForm, Form
from .models import Submission, Journal
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from django import forms

class JournalForm(ModelForm):
    """
    This class bridges the model created in JournalSubmission/models of a Journal entry in the database
    to an actual html form that the editor can submit when ready to construct a journal
    """

    class Meta:
        model = Journal
        fields = ['title', 'subject']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'SUBMIT'))


class SubmissionForm(ModelForm):
    """
    This class bridges the model created in JournalSubmission/models of a submission entry in the database
    to an actual html form that the user can submit when ready to upload their work
    """

    class Meta:
        model = Submission
        fields = ['journal', 'title', 'file', 'reviewer1', 'reviewer2', 'reviewer3']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'SUBMIT'))



    # All notify functions will be called upon an author submitting!

    def notify_editor(self, submission):
        """
        PRECONDITION: Submission form submitted of their work. Form was validated

        Given that the submission object parameter was just posted, notify the editor of the journal specified
        :param submission: the model of the submission that was just posted
        :return: void
        """

        # Get the journal

        # Get the editor of the journal

        # Add new submission to the editors list of new submissions.


        return


    def notify_reviewers(self, submisison):
        """
        PRECONDITION: The Editor confirmed the submission and added any new editors. He/She also confirmed
                        the reviewers for this post are relevant.

        Given that the submission object parameter was just posted, notify the editor of the journal specified
        :param submission: the model of the submission that was just posted
        :return: void
        """


        return


class EditorAccept(ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'reviewer1', 'reviewer2', 'reviewer3']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'SUBMIT'))


class ReviewerForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'SUBMIT'))

    accept = forms.TypedChoiceField(
        label = "Please choose whether you believe this journal should publish this work:",
        choices = ((1, "ACCEPT"), (0, "REJECT")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '0',
        required = True,
    )

    comment = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="IF you are rejecting the work, give specific feedback as to where the author can improve."
        )

