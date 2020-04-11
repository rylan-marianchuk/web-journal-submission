from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from JournalSubmission.forms import JournalForm, EditorAccept, ReviewerForm
from .decorators import user_unauthenticated
from .forms import CreateUserForm, ProfileDetailsForm
from .query import *
from django.contrib.auth.models import Group


@user_unauthenticated
def register_page(request):
    """
    The register_page function allows users to be added to groups dynamically based on role
    selected when registering for the web application. Important, the database must have groups pre created
    as follows for this to work: 'Author', 'Editor', 'Reviewer'
    """
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        form_profile = ProfileDetailsForm(request.POST)
        if form.is_valid() and form_profile.is_valid():
            user = form.save()
            profile = form_profile.save(commit=False)
            profile.user = user
            profile.save()
            user_data = form_profile['role'].value()

            if user_data == 'author':
               group = Group.objects.get(name='Author')
               user.groups.add(group)
            elif user_data == 'editor':
                group = Group.objects.get(name='Editor')
                user.groups.add(group)
            elif user_data == 'reviewer':
                group = Group.objects.get(name='Reviewer')
                user.groups.add(group)
            user_name = form.cleaned_data.get('username')
            messages.success(request, 'Account created for ' + user_name)
            return redirect('login')
    else:
        form = CreateUserForm()
        form_profile = ProfileDetailsForm()
    context = {'form': form, 'form_profile': form_profile}
    return render(request, 'users/register.html', context)


@user_unauthenticated
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'users/login.html', context)



def logout_user(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def displayProfile(request, pk):
    """
    Obtain the database entry from the specified primary key. This data is to display the user on the profile page.
    :param request:
    :param pk: the primary key of the user sending the request. Use this for querying into the Profile database
    :return: the rendering of the profile page.
    """


    # Get the user databse object of the profile request
    profile_db = getProfile(pk)

    context = {"profile": profile_db}

    # Get the context for each case of the user role
    if profile_db.role == "author":
        context.update(getContextForAuthor(profile_db))
    elif profile_db.role == 'editor':
        context.update(getContextForEditor(profile_db, request.method == "POST", request))
    elif profile_db.role == 'reviewer':
        context.update(getContextForReviewer(profile_db, request.method == "POST", request))

    return render(request, 'users/profile.html', context)



def getContextForEditor(profile_db, posting, request):
    """
    Acquire all required data to display the editors profile page

    :param profile_db: the profile model of this user
    :param posting: bool whether this display request is a posting of a form
    :param request: this request object
    :return: the context dictionary, the info to pass to html file
    """

    context = {}
    # Make a query by editor to see if this editor has already created a journal

    if len(getJournal(profile_db)) == 0:

        # Check if the display request was a post
        if posting:
            base_journal = Journal(editor=profile_db)
            form = JournalForm(request.POST, instance=base_journal)
            if form.is_valid():
                form.save()
                return getContextForEditor(profile_db, False, request)
            else:
                messages.info(request, 'This form is invalid')
        context["hasJournal"] = False
        context["journalForm"] = JournalForm()
        return context

    # If here gotten the journal object.


    # Get all submissions made for this journal that are pending and display in editor profile
    context["hasJournal"] = True
    toApprove = getSubmissionsEditor(getJournal(profile_db)[0], editorApproved=False)


    # Check if editor posted something.
    if posting:
        # If true, then it must be the case that toApprove (the result of the query for submissions to his journal),
        # is not null
        form = EditorAccept(request.POST)
        if form.is_valid():
            # Update the submission object
            toApprove.reviewer1 = getProfile_id(int(form.data['reviewer1']))
            toApprove.reviewer2 = getProfile_id(int(form.data['reviewer2']))
            toApprove.reviewer3 = getProfile_id(int(form.data['reviewer3']))
            toApprove.editorApproved = True
            toApprove.inReview = True
            toApprove.save()
            return getContextForEditor(profile_db, False, request)
        else:
            messages.info(request, 'This form is invalid')

    if toApprove != None:
        # Then there exists some submission to his Journal
        context["toApprove"] = True
        # Create the form and attatch it to the model.
        context["approveForm"] = EditorAccept(initial={'reviewer1': toApprove.reviewer1,
                                                  'reviewer2': toApprove.reviewer2,
                                                  'reviewer3': toApprove.reviewer3,
                                                  'title': toApprove.title})
    else:
        context["toApprove"] = False

    # The list of submissions the editor has accepted to reviewers. This is mainly
    # to display status with no functionality
    context["statusOfApproved"] = getSubmissionsJournal(getJournal(profile_db)[0], editorApproved=True)
    return context


def getContextForAuthor(profile_db):
    """
    Acquire all required data to display the authors profile page

    :param profile_db: the profile model of this user
    :return: the context dictionary, the info to pass to html file
    """
    context = {}
    context["submissionLISTreviewing"] = getSubmissionsAUTHOR(profile_db, True)
    context["submissionLISTdone"] = getSubmissionsAUTHOR(profile_db, False)
    return context


def getContextForReviewer(profile_db, posting, request):
    """
    Acquire all required data to display the Reviewers profile page

    :param profile_db: the profile model of this user
    :param posting: bool whether this display request is a posting of a form
    :param request: this request object
    :return: the context dictionary, the info to pass to html file
    """

    context = {'reviewer_form': ReviewerForm(), 'hasReview': False}

    toReview, reviewer_number = getSubmissionsToReview(profile_db.id)

    if posting:
        # If true, then it must be the case that toRemove (the result of the query for submissions including this reviewer),
        # is not null
        form = ReviewerForm(request.POST)
        if form.is_valid():
            # Add this reviewer number to the set of reviewers seen on this submission object
            toReview.reviewed(reviewer_number, int(request.POST['accept']))
            if int(request.POST['accept']):
                reviewerAccept(toReview)
            else:
                reviewerReject(toReview, request.POST['comment'], reviewer_number)
        return getContextForReviewer(profile_db, False, request)



    if toReview == None:
        return context

    # There exists submissions for this reviewer, found by the query
    context['hasReview'] = True
    context['toReview'] = toReview
    return context


def reviewerAccept(toReview):
    """
    Update the submission object given that a reviewer has accepted their submission.

    :param toReview: the submission object that is being reviewed
    :param reviewer_number: the number in [1, 3] of this reviewer
    :return:
    """

    # IF this acceptance post was the final review and NO ONE rejected, this article has been accepted,
    # i.e. is no longer in review.
    if toReview.isReviewed() and sum([1 for i in range(1, 4) if toReview.didReject(i)]) == 0:
        toReview.inReview = False
    elif toReview.isReviewed():
        toReview.feedbackReady = True
        toReview.resubmissions_remaining -= 1
    toReview.save()
    return


def reviewerReject(toReview, comment, reviewer_id):
    """
    Update the submission object given that a reviewer has rejected their submission.

    :param toReview: the submission object that is being reviewed
    :param reviewer_id: the number of this reviewer inclusive of [1,3]
    :param comment: the text the reviewer gave as feedback for rejection
    :return:
    """


    if reviewer_id == 1:
        toReview.reviewer1_FEED = comment
    if reviewer_id == 2:
        toReview.reviewer2_FEED = comment
    if reviewer_id == 3:
        toReview.reviewer3_FEED = comment

    # If this was the last reviewer to reject: put feedback ready
    if toReview.isReviewed():
        toReview.feedbackReady = True
        toReview.resubmissions_remaining -= 1
        if toReview.resubmissions_remaining == 0:
            toReview.rejected = True
            toReview.inReview = False

    toReview.save()
    return
