from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import Submission
from .forms import SubmissionForm
from django.shortcuts import render, redirect
from users.models import Profile
# Create your views here.


def homePage(request):
    return render (request, 'JournalSubmission/home.html')

def successMessage(request):
    return render(request, 'JournalSubmission/success_message.html')


def journalList(request):
    """
    Render the home page which is a list of journals. Each journal should be linked to their own page.

    :param request:
    :return:
    """
    return render (request, 'JournalSubmission/journalList.html')


def displayJournal(request):
    """

    :param request:
    :return:
    """
    # Get the journal object from the database
    context = None

    return render(request, "JournalSubmission/journal.html", context)



def newSubmission(request, *args, **kwargs):
    """
    The view to be called when a user clicks on the new submission button on their profile.
    """
    submitting_user = kwargs['user']

    if request.method == "POST":
        # Generate the submission form object to save to the database
        # MUST have request.FILES as a parameter to save the upload, otherwise the form will be invalid when submitted
        author = Profile.objects.get(user=User.objects.get(username=submitting_user))
        base_submisison = Submission(author=author)
        form = SubmissionForm(request.POST, request.FILES, instance=base_submisison)
        if form.is_valid() and selfValidate(form):
            form.save()
            form.notify_editor(form)
        return redirect('success_message')
    else:
        form = SubmissionForm()
    return render(request, 'JournalSubmission/submission.html', {'form':form})



def selfValidate(form):
    """
    Manual validation function of a submission form

    Display helpful error messages when the form fails validaiton criterion

    :param form: the model form object of the current submission just made by the author
    :return: bool whether the form satisfies the valid criteria proposed
    """

    is_valid = True
    # Ensure all reviewers are unique

    # Ensure the file type was a pdf

    return is_valid