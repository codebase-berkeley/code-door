from django.shortcuts import render, redirect, get_object_or_404
from codedoor.models import Profile, Company, Question, Application
from django.http import HttpResponse
from codedoor.models import Review, Company, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def search(request, database):
    input_query = request.POST['query']
    parsed_query = input_query.split(" ")
    query = None
    if parsed_query:
        query = parsed_query[0]
    for q in parsed_query[1:]:
        query = query and SearchQuery(q)

    review_vector = SearchVector('company__name', 'reviewer__user__first_name', 'reviewer__user__last_name',
                                 'title')
    application_vector = SearchVector('company__name', 'profile__user__first_name', 'profile__user__last_name',
                                      'position')
    company_vector = SearchVector('name', 'industry')
    profile_vector = SearchVector('user__first_name', 'user__last_name', 'current_job')
    if database == "reviews":
        vector = review_vector
        entry = Review.objects.annotate(search=vector).filter(search=query)
    elif database == "interviews":
        vector = application_vector
        entry = Application.objects.annotate(search=vector).filter(search=query)
    elif database == "companies":
        vector = company_vector
        entry = Company.objects.annotate(search=vector).filter(search=query)
    elif database == "users":
        vector = profile_vector
        entry = Profile.objects.annotate(search=vector).filter(search=query)
    paginator = Paginator(entry, 10)
    page = request.GET.get('page', 1)
    data = pagination(paginator, page)

    return render(request, "codedoor/search.html", {"database": database, "data": data, "query": input_query})

'''
def reviews_filter(request, company):
    input_rating = request.POST['rating']
    input_recommend = request.POST['recommend']

    entry = Review.objects.filter(company=company, rating=input_rating, recommend=input_recommend)

    paginator = Paginator(entry, 4)
    page = request.GET.get('page', 1)
    data = pagination(paginator, page)

    return render(request, "codedoor/viewcompany.html", {"reviews": data, "rating": input_rating,
                                                         "recommend": input_recommend})


def interviews_filter(request, company):
    input_year = request.POST['year']
    input_season = request.POST['season']
    input_received_offer = request.POST['received_offer']

    entry = Application.objects.filter(company=company, year=input_year, season=input_season,
                                       received_offer=input_received_offer)

    paginator = Paginator(entry, 4)
    page = request.GET.get('page', 1)
    data = pagination(paginator, page)

    return render(request, "codedoor/viewcompany.html", {"applications": data, "year": input_year, "season": input_season,
                                                         "received_offer": input_received_offer})
'''

def pagination(paginator, page):
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)
