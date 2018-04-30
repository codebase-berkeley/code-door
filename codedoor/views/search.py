from django.shortcuts import render, redirect, get_object_or_404
from codedoor.models import Profile, Company, Question, Application
from django.http import HttpResponse
from codedoor.models import Review, Company, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

RESULTS_PER_PAGE = 5


def search(request, database):
    input_query = request.GET.get('query')
    parsed_query = input_query.split("+")

    query = None
    if parsed_query:
        query = parsed_query[0]
    for q in parsed_query[1:]:
        query = query and SearchQuery(q)

    review_vector = SearchVector('company__name', 'reviewer__user__first_name', 'reviewer__user__last_name',
                                 'title')
    application_vector = SearchVector('company__name', 'profile__user__first_name', 'profile__user__last_name',
                                      'position')
    company_vector = SearchVector('name')
    profile_vector = SearchVector('user__first_name', 'user__last_name', 'current_job')
    if database == "reviews":
        vector = review_vector
        entry = Review.objects.annotate(search=vector, rank=SearchRank(vector, query)).filter(search=query).order_by('-rank')
    elif database == "interviews":
        vector = application_vector
        entry = Application.objects.annotate(search=vector, rank=SearchRank(vector, query)).filter(search=query).order_by('-rank')
    elif database == "companies":
        vector = company_vector
        entry = Company.objects.annotate(search=vector, rank=SearchRank(vector, query)).filter(search=query).order_by('-rank')
    elif database == "users":
        vector = profile_vector
        entry = Profile.objects.annotate(search=vector, rank=SearchRank(vector, query)).filter(search=query).order_by('-rank')
    n = len(entry)
    paginator = Paginator(entry, RESULTS_PER_PAGE)
    page = request.GET.get('page', 1)

    def pagination(paginator, page):
        try:
            return paginator.page(page)
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return paginator.page(paginator.num_pages)
    data = pagination(paginator, page)

    return render(request, "codedoor/search.html", {"database": database, "data": data, "number": n,
                                                    "query": input_query})
