from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse

from JournalSubmission.models import Journal
from JournalSubmission.forms import JournalForm
from .forms import CreateUserForm, ProfileDetailsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import user_unauthenticated
from .query import *
from django.contrib.auth.models import Group

'''Still few tweaks are required like error message handling, redirect, and so on'''

@user_unauthenticated
def register_page(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        form_profile = ProfileDetailsForm(request.POST)
        if form.is_valid() and form_profile.is_valid():
            user = form.save()
            profile = form_profile.save(commit=False)
            profile.user = user
            profile.save()
            user_data = form_profile['role'].value()
            #testing purposes 'print'
            print(user_data)
            #user automatically added to chosen role group in the backend

            if user_data == 'author':
               group = Group.objects.get(name='Author')
               user.groups.add(group)
            elif user_data == 'editor':
                group = Group.objects.get(name='Editor')
                user.groups.add(group)
            elif user_data == 'reviewer':
                group = Group.objects.get(name='Reviewer')
                user.groups.add(group)

            #messages.success(request, 'success')
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

            return render(request, 'JournalSubmission/home.html')
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

    if request.method == "POST":
        base_journal = Journal(editor=profile_db)
        form = JournalForm(request.POST, instance=base_journal)
        if form.is_valid():
            form.save()
        else:
            raise Exception("Please catch these invalid forms")



    context = {"profile": profile_db}

    # Get the submissions of the author
    if profile_db.role == "author":
        context["submissionLISTreviewing"] = getSubmissionsAUTHOR(profile_db, True)
        context["submissionLISTdone"] = getSubmissionsAUTHOR(profile_db, False)
    if profile_db.role == 'editor':
        try:
            # Make a query by editor to see if this editor has already created a journal
            journal_db = getJournal(profile_db)

            # If here gotten the journal object.
            # Get all submissions made for this journal that are pending and display in editor profile
            context["hasJournal"] = True
        except:
            context["hasJournal"] = False
            context["journalForm"] = JournalForm()

    return render(request, 'users/profile.html', context)


