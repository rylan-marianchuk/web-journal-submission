from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm, LoginForm
from users.models import User

def register(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            newUser = form.save(commit=False)
            newUser.user = request.user
            newUser.save()

            #users = User.objects.all()

            return redirect('profile')
    else:
        formObj = UserForm
        return render(request, "users/register.html", {'form': formObj})



def profile(request):
    return render(request, "users/profile.html")

def login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect('profile')

    else:
        formObj = LoginForm
        return render(request, "users/login.html")
