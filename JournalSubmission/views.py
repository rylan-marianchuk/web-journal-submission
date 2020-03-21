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

def journalList(request):
    return render (request, 'JournalSubmission/journalList.html')

def successMessage(request):
    return render(request, 'JournalSubmission/success_message.html')

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
        if form.is_valid():
            form.save()
        return redirect('success_message')
    else:
        form = SubmissionForm()
    return render(request, 'JournalSubmission/submission.html', {'form':form})


