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
    reviews = Review.objects.all().order_by('-pk')[:3]
    applications = Application.objects.all().order_by('-id')[:3]
    num_reviews = Review.objects.all().count()
    num_apps = Application.objects.all().count()
    companies = [Company.objects.get(id=review.company.id) for review in reviews]
    companies += [Company.objects.get(id=application.company.id) for application in applications]
    top_profiles = Profile.objects.all().order_by('-codebucks')[:3]

    return render(
        request,
        "codedoor/home.html",
        {
            "applications": applications,
            "companies": companies,
            "is_home": True,
            "num_reviews": num_reviews,
            "num_apps": num_apps,
            "reviews": reviews,
            "top_profiles": top_profiles
        }
    )

@login_required
def codebank(request):
    """
    Display the codebucks leaderboards.
    :param request:
    :return:
    """
    top_profiles = Profile.objects.all().order_by('-codebucks')[:3]

    return render(request, "codedoor/codebank.html", { "top_profiles": top_profiles })
