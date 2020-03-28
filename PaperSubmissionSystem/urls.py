"""PaperSubmissionSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_Views
from JournalSubmission import views as journal_Views


urlpatterns = [
    path('', journal_Views.homePage, name='home'),
    path('admin/', admin.site.urls),

    # User Authentication URLS
    path('register/', user_Views.register_page, name= 'register'),
    #path('profile/', user_Views.displayProfile, name= 'profile'),
    path('login/', user_Views.login_page, name= 'login'),
    path('logout/', user_Views.logout_user, name= 'logout'),
    path('profile/(?P<pk>)/$', user_Views.displayProfile, name= 'profile'),

    #Journal URLS
    path('submission/(?P<user>)/$', journal_Views.newSubmission, name= 'submission'),
    path('success_message/', journal_Views.successMessage, name='success_message'),
    path('journals/', journal_Views.journalList, name='journals')
]
