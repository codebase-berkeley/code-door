from django.shortcuts import render, redirect, get_object_or_404
from codedoor.models import Profile, Company, Question, Application
from django.http import HttpResponse
from codedoor.models import Review, Company, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


def search(request, database):
    review_vector = SearchVector('company__name', 'reviewer__user__first_name', 'reviewer__user__last_name',
                                 'title')
    application_vector = SearchVector('company__name', 'profile__user__first_name', 'profile__user__last_name',
                                      'position')
    company_vector = SearchVector('name', 'industry')
    profile_vector = SearchVector('user__first_name', 'user__last_name', 'current_job')
    if database == "reviews":
        vector = review_vector
    elif database == "applications":
        vector = application_vector
    elif database == "companies":
        vector = company_vector
    elif database == "profiles":
        vector = profile_vector
    input_query = request.POST['query']
    parsed_query = input_query.split(" ")
    query = None
    if parsed_query:
        query = parsed_query[0]
    for q in parsed_query[1:]:
        query = query and SearchQuery(q)

    entry = Entry.objects.annotate(vector).filter(search=query)
    # review_entry = Entry.objects.annotate(review_vector).filter(search=query)
    # application_entry = Entry.objects.annotate(application_vector).filter(search=query)
    # company_entry = Entry.objects.annotate(company_vector).filter(search=query)
    # profile_entry = Entry.objects.annotate(profile_vector).filter(search=query)

    paginator = Paginator(entry, 10)
    # review_paginator = Paginator(review_entry, 3)
    # application_paginator = Paginator(application_entry, 3)
    # company_paginator = Paginator(company_entry, 3)
    # profile_paginator = Paginator(profile_entry, 3)
    page = request.GET.get('page', 1)
    def pagination(paginator, page):
        try:
            return paginator.page(page)
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return paginator.page(paginator.num_pages)

    list = pagination(paginator, page)
    # review_list = pagination(review_paginator, page)
    # application_list = pagination(application_paginator,page)
    # company_list = pagination(company_paginator, page)
    # profile_list = pagination(profile_paginator,page)

    return render(request, "codedoor/search.html", {"database": list})



