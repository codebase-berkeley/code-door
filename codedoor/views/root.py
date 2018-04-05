from django.shortcuts import render, redirect, get_object_or_404
from codedoor.models import Profile, Company, Question, Application
from django.http import HttpResponse

from codedoor.models import Review, Company, Profile
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


def home(request):
    reviews = Review.objects.all().order_by('-id')[:6]
    applications = Application.objects.all()
    paginator = Paginator(reviews, 3)
    page = request.GET.get('page', 1)
    try:
        review_list = paginator.page(page)
    except PageNotAnInteger:
        review_list = paginator.page(1)
    except EmptyPage:
        review_list = paginator.page(paginator.num_pages)


    return render(request, "codedoor/home.html", {"reviews": review_list, "applications": applications})

