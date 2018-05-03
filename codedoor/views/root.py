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
    actual_companies = Company.objects.all()

    return render(request, "codedoor/home1.html", {"actual_companies": actual_companies, "companies": companies, "reviews": reviews, "applications": applications, "num_reviews": num_reviews, "num_apps": num_apps, "is_home": True})

