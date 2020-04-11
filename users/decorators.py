from django.http import HttpResponse
from django.shortcuts import redirect


'''This is a custom decorator which allows to prevent login or register htmls to be 
rendered to user if user is authenticated and redirects to journals page
---else executes if user is authenticated, the view_func is passed through function below decorator in views.py'''

def user_unauthenticated(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


