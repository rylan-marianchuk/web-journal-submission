from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def homePage(request):
    return render (request, 'JournalSubmission/home.html')

def journalList(request):
    return render(request, 'JournalSubmission/journalList.html')