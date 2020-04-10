from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import Submission, Journal
from .forms import SubmissionForm, ResubmissionForm
from django.shortcuts import render, redirect
from users.models import Profile
from django.contrib import messages
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

    context = {
        "health" : list(Journal.objects.filter(subject="health & medicine")),
        'humanities' : list(Journal.objects.filter(subject="humanities")),
        'mathematics' : list(Journal.objects.filter(subject="mathematical sciences")),
        'social_sciences' : list(Journal.objects.filter(subject="social sciences")),
        'physical_sciences' : list(Journal.objects.filter(subject="physics"))
    }
    return render (request, 'JournalSubmission/journalList.html', context)


def displayJournal(request, *args, **kwargs):
    """

    :param request:
    :return:
    """
    # Get the journal object from the database
    journal_string = kwargs['journal']
    idnumber = Journal.objects.filter(title = journal_string)[0].id
    subList = list(Submission.objects.filter(journal = idnumber, inReview = False, editorApproved = True,
                              rejected = False))

    context = {'accepted': subList, 'journal': Journal.objects.filter(title = journal_string)[0]}

    return render(request, "JournalSubmission/journal.html", context)



def newSubmission(request, *args, **kwargs):
    """
    The view to be called when a user clicks on the new submission button on their profile.
    """
    submitting_user = kwargs['user'].split(" ")[0]

    if request.method == "POST":
        # Generate the submission form object to save to the database
        # MUST have request.FILES as a parameter to save the upload, otherwise the form will be invalid when submitted
        author = Profile.objects.get(user=User.objects.get(username=submitting_user))
        base_submisison = Submission(author=author)
        form = SubmissionForm(request.POST, request.FILES, instance=base_submisison)
        if form.is_valid():
            form.save(commit=False)
            user_1 = form.cleaned_data['reviewer1']
            user_2 = form.cleaned_data['reviewer2']
            user_3 = form.cleaned_data['reviewer3']
            if user_2 == user_1 or user_2 == user_3 or user_1 == user_3:
                messages.error(request, "Invalid Reviewer selection, choose a reviewer only once.")
                form = SubmissionForm()
            else:
                form.save()
                return redirect('success_message')
    else:
        form = SubmissionForm()
    return render(request, 'JournalSubmission/submission.html', {'form':form})



def seeFeedback(request, *args, **kwargs):
    """
    The view to be called when a user clicks on the new submission button on their profile.

    Displays the comments from each reviewer if they decided to reject the authors submission

    Add an upload button at the end of the page only if there are resubmissions remaining for the author
    to reupload their pdf of incorporated changes.
    """
    submission_name = kwargs['submission']

    # Query to get this submission object
    submission = Submission.objects.get(title=submission_name)

    if request.method == "POST":
        # Incorporate a resubmission form
        resub_form = ResubmissionForm(request.POST, request.FILES, instance=submission)
        if resub_form.is_valid():
            resub_form.save()
            resubmitted(submission)
            return redirect('success_message')

    resub_form = ResubmissionForm()
    context = {'rev1Rejected': submission.didReject(1), 'rev2Rejected':  submission.didReject(2),
               'rev3Rejected':  submission.didReject(3)}
    context.update({'submission' : submission, "form": resub_form})

    return render(request, 'JournalSubmission/feedback.html', context)


def resubmitted(submission):
    """
    Reset all submission values necessary for a resubmisison.

    Note the integer resubmissions remaining has already been decremented
    :param submission:
    :return:
    """

    submission.seen_accept = ""
    submission.feedbackReady = False
    submission.reviewer1_FEED = ""
    submission.reviewer2_FEED = ""
    submission.reviewer3_FEED = ""
    submission.save()
    return