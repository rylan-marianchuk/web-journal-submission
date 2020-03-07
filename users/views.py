from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm
from users.models import User

def register(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            newUser = form.save(commit=False)
            newUser.user = request.user
            newUser.save()

            #users = User.objects.all()

            return render(request, 'users/login.html')
    else:
        formObj = UserForm
        return render(request, "users/register.html", {'form': formObj})