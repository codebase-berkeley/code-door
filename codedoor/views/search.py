from django.shortcuts import render, redirect, get_object_or_404
from codedoor.models import Profile, Company, Question, Application
from django.http import HttpResponse
from codedoor.models import Review, Company, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


def search(request, database, text):
    if request.method == "GET":
    if database == "Review":
        vector = SearchVector('company__name', 'reviewer__user__first_name', 'reviewer__user__last_name', 'title')
    elif database == "Application":
        vector = SearchVector('company__name', 'profile__user__first_name', 'profile__user__last_name', 'position')
    elif database == "Company":
        vector = SearchVector('name', 'industry')
    elif database == "Profile":
        vector = SearchVector('user__first_name', 'user__last_name', 'current_job')


Entry.objects.annotate(search).filter(search=text)
    parsed_text =
    query = SearchQuery(text)

if request.method == "GET":
    return render(request, 'codedoor/createprofile.html')
else:
    try:
        input_username = request.POST['email']
        input_password = request.POST['password']
        input_email = request.POST['email']
        input_first_name = request.POST['first_name']
        input_last_name = request.POST['last_name']
        input_profile_pic = request.FILES['profile_pic'].read()
        input_graduation_year = request.POST['graduation_year']
        input_current_job = request.POST['current_job']
        input_linkedin = request.POST['linkedin']
        if "http://" not in input_linkedin and "https://" not in input_linkedin and input_linkedin:
            input_linkedin = "http://" + input_linkedin
        # input_resume = request.POST['resume']
    except Exception as e:
        return HttpResponse("You did not fill out the form correctly!")