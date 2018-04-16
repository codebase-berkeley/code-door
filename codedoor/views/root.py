from django.shortcuts import render, redirect, get_object_or_404
from codedoor.models import Profile, Company, Question, Application
from django.http import HttpResponse

from codedoor.models import Review, Company, Profile
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


@login_required
def home(request):
    if request.method == "GET":
        reviews = Review.objects.all().order_by('-id')
        applications = Application.objects.all().order_by('-id')
        paginator_1 = Paginator(reviews, 3)
        paginator_2 = Paginator(applications, 3)
        page = request.GET.get('page', 1)
        try:
            review_list = paginator_1.page(page)
        except PageNotAnInteger:
            review_list = paginator_1.page(1)
        except EmptyPage:
            review_list = paginator_1.page(paginator_1.num_pages)
        try:
            application_list = paginator_2.page(page)
        except PageNotAnInteger:
            application_list = paginator_2.page(1)
        except EmptyPage:
            application_list = paginator_2.page(paginator_2.num_pages)
        return render(request, "codedoor/home.html", {"reviews": review_list, "applications": application_list})
    else:
        try:
            input_query = request.get("input_query")
            parsed_query = input_query.split(" ")
            query = ""
            for q in parsed_query:
                query = str(q) + "_"
            query -= "_"
            return redirect("codedoor:search", query=query)


def search(request, database, text):
    review_vector = SearchVector('company__name', 'reviewer__user__first_name', 'reviewer__user__last_name', 'title')
    application_vector = SearchVector('company__name', 'profile__user__first_name', 'profile__user__last_name',
                                      'position')
    company_vector = SearchVector('name', 'industry')
    profile_vector = SearchVector('user__first_name', 'user__last_name', 'current_job')

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
    parsed_text = input
    query = SearchQuery(text)
