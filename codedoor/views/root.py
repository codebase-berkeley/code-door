from django.shortcuts import render, redirect, get_object_or_404
from codedoor.models import Profile, Company, Question, Application
from django.http import HttpResponse

def home(request):
  applications = Application.objects.all()
  return render(request, "codedoor/dashboard.html", {"applications": applications})
