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
    reviews = Review.objects.all()[:3]
    applications = Application.objects.all().order_by('-id')
    companies = Company.objects.all()
    paginator_2 = Paginator(applications, 3)
    page = request.GET.get('page', 1)

    try:
        application_list = paginator_2.page(page)
    except PageNotAnInteger:
        application_list = paginator_2.page(1)
    except EmptyPage:
        application_list = paginator_2.page(paginator_2.num_pages)

    return render(request, "codedoor/home.html", {"companies": companies, "reviews": reviews, "applications": application_list})
