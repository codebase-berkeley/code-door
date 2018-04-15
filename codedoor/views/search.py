from django.shortcuts import render, redirect, get_object_or_404
from codedoor.models import Profile, Company, Question, Application
from django.http import HttpResponse
from codedoor.models import Review, Company, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


def search(request, database, text):
    if database == "Review":
        vector = SearchVector('company__name', 'reviewer__user__first_name', 'reviewer__user__last_name', 'title')
    elif database == "Application":
        vector = SearchVector('company__name', 'profile__user__first_name', 'profile__user__last_name', 'position')
    elif database == "Company":
        vector = SearchVector('name', 'industry')
    elif database == "Profile":
        vector = SearchVector('user__first_name', 'user__last_name', 'current_job')

    parsed_text =
    query = SearchQuery(text)