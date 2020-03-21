from django.forms import ModelForm
from .models import Submission
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper


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

