from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import CreateUserForm, ProfileDetailsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import user_unauthenticated

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
            return redirect('profile')
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'users/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile_page(request):
    context = {}
    return render(request, "users/profile.html", context)

