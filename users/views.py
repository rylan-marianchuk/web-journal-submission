from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import CreateUserForm, ProfileDetailsForm
from django.contrib.auth import authenticate, login, logout

'''Still few tweaks are required like error message handling, redirect, and so on'''
def register_page(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        form_profile = ProfileDetailsForm(request.POST)
        if form.is_valid() and form_profile.is_valid():
            user = form.save()
            profile = form_profile.save(commit=False)
            profile.user = user
            profile.save()
            #messages.success(request, 'success')
            return redirect('login')
    else:
        form = CreateUserForm()
        form_profile = ProfileDetailsForm()
    context = {'form': form, 'form_profile': form_profile}
    return render(request, 'users/register.html', context)

def login_page(request):
    login_failed = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'Username or Password is incorrect')
            login_failed = True
    context = { 'loginfailed': login_failed }
    return render(request, 'users/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')


def profile_page(request):
    context = {}
    return render(request, "users/profile.html", context)

