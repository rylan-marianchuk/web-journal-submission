from django.forms import ModelForm
from .models import Submission, Journal
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from django import forms
from users.models import Profile

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
        self.user = kwargs.pop('user', None)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'SUBMIT'))

        self.fields['reviewer1'].queryset = Profile.objects.filter(role='reviewer')
        self.fields['reviewer2'].queryset = Profile.objects.filter(role='reviewer')
        self.fields['reviewer3'].queryset = Profile.objects.filter(role='reviewer')

class ResubmissionForm(ModelForm):
    """
    This class bridges the model created in JournalSubmission/models of a submission entry in the database
    to an actual html form that the user can submit when ready to upload their work
    """

    class Meta:
        model = Submission
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'SUBMIT'))


class EditorAccept(ModelForm):
    """
    When an author submits to an editor's journal, this form will be prompted to the editor to confirm
    all is correct. The submission of this form will send the paper to its respective reviewers.
    """
    class Meta:
        model = Submission
        fields = ['title', 'reviewer1', 'reviewer2', 'reviewer3']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'SUBMIT'))

        self.fields['reviewer1'].queryset = Profile.objects.filter(role='reviewer')
        self.fields['reviewer2'].queryset = Profile.objects.filter(role='reviewer')
        self.fields['reviewer3'].queryset = Profile.objects.filter(role='reviewer')


class ReviewerForm(forms.Form):
    """
    The form for reviewers to give their feedback on submission. They must choose a bool whether they believe it
    should be rejected or not. If rejected, they must provide feedback in the text area char field.
    """


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

