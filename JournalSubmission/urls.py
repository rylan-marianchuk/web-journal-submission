from django.urls import path
from . import views
urlpatterns = [
    path('', views.homePage, name='home'),
    path('journals/', views.journalList, name='journals')
]
