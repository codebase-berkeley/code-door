from codebank.utils import add_codebucks
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.core.paginator import Paginator
from django.core import serializers
from django.contrib.auth.decorators import login_required

from codedoor.models import Profile, Company, Question, Application, ApplicationComment, User

import traceback

@login_required
def create_application(request, companypk):
    """
    POST route for when the user creates an application.
    This route contains the company PK in the route URL.
    TODO replace with Django-REST-Framework API routes.
    """
    applicant_profile = request.user.profile
    profilepk = applicant_profile.pk
    if request.method == 'POST':
        try:
            description = request.POST['description']
            season = request.POST['season']
            position = request.POST['position']
            received_offer = request.POST['received_offer']
            year = request.POST['year']
            if(received_offer == "Yes"):
                received_offer = True
            else:
                received_offer = False
            offer_details = request.POST['offer_details']
            difficulty = request.POST['difficulty']
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({})
        a = Application(
            company=Company.objects.get(pk=companypk),
            profile=Profile.objects.get(pk=profilepk),
            description=description,
            season=season,
            position=position,
            received_offer=received_offer,
            offer_details=offer_details,
            difficult=difficulty,
            year=year
        )
        a.save()
        # add codebucks to the applicant profile.
        add_codebucks(applicant_profile, 150)

        return JsonResponse({
            "a": serializers.serialize('json', Application.objects.filter(pk=a.pk)),
            "c": serializers.serialize('json', Company.objects.filter(pk=a.company.pk)),
            "p": serializers.serialize('json', Profile.objects.filter(pk=a.profile.pk)),
            "u": serializers.serialize('json', User.objects.filter(pk=a.profile.user.pk))
        }, safe=False)
    return Http404("No such page exists")


@login_required
def create_application_company(request):
    """
    POST route for when the user creates an application.
    The company PK is included in the POST payload.
    TODO replace with Django-REST-Framework API routes.
    """
    applicant_profile = request.user.profile
    profilepk = applicant_profile.pk
    companies = Company.objects.filter()
    if request.method == 'POST':
        try:
            companypk = request.POST['company']
            description = request.POST['description']
            season = request.POST['season']
            position = request.POST['position']
            received_offer = request.POST['received_offer']
            year = request.POST['year']
            if(received_offer == "Yes"):
                received_offer = True
            else:
                received_offer = False
            offer_details = request.POST['offer_details']
            difficulty = request.POST['difficulty']
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({})
        a = Application(
            company=Company.objects.get(pk=companypk),
            profile=Profile.objects.get(pk=profilepk),
            description=description,
            season=season,
            position=position,
            received_offer=received_offer,
            offer_details=offer_details,
            difficult=difficulty,
            year=year
        )
        a.save()
        # add codebucks to the applicant profile.
        add_codebucks(applicant_profile, 150)

        return JsonResponse({
            "a": serializers.serialize('json', Application.objects.filter(pk=a.pk)),
            "c": serializers.serialize('json', Company.objects.filter(pk=a.company.pk)),
            "p": serializers.serialize('json', Profile.objects.filter(pk=a.profile.pk)),
            "u": serializers.serialize('json', User.objects.filter(pk=a.profile.user.pk))
        }, safe=False)
    return Http404("No such page exists")

@login_required
def edit_application(request, pk):
    a = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        try:
            a.description = request.POST['description']
            a.season = request.POST['season']
            a.position = request.POST['position']
            received_offer = request.POST['received_offer']
            a.year = request.POST['year']
            if(received_offer):
                a.received_offer = True
            else:
                a.received_offer = False
            a.offer_details = request.POST['offer_details']
            a.difficult = request.POST['difficulty']
        except Exception as e:
            traceback.print_exc()
            return HttpResponse("You did not fill out the form correctly")
        a.save()
        return JsonResponse({})
    return HttpResponse("couldn't edit the application")


def view_application(request, pk):
    a = get_object_or_404(Application, pk=pk)
    profile = get_object_or_404(Profile, id=a.profile.pk)
    questions = Question.objects.filter(application=pk).order_by("-pk")
    return render(request, "codedoor/view_application.html", {"a": a, "profile" : profile, "questions": questions})


def list_applications(request, pk, pg=1):
    applications = Application.objects.filter(company=pk).order_by("-pk")
    paginator = Paginator(applications, 5)
    page = request.GET.get('page', 1)
    try:
        applications_list = paginator.page(page)
    except PageNotAnInteger:
        applications_list = paginator.page(1)
    except EmptyPage:
        applications_list = paginator.page(paginator.num_pages)

    return render(
        request,
        "codedoor/list_applications.html",
        {
            "applications": applications,
            "page": applications_list
        }
    )

def list_all_applications(request, pg=1):
    companies = Company.objects.all()
    applications = Application.objects.order_by("-pk")
    paginator = Paginator(applications, 10)
    page = request.GET.get('page', 1)
    try:
        applications_list = paginator.page(page)
    except PageNotAnInteger:
        applications_list = paginator.page(1)
    except EmptyPage:
        applications_list = paginator.page(paginator.num_pages)

    return render(
        request,
        "codedoor/list_applications.html",
        {
            "applications": applications,
            "page": applications_list,
            "companies": companies
        }
    )

def created_question(request):
    if request.method == "POST":

        question = request.POST['question']
        company_answer = request.POST['company_answer']
        app_answer = request.POST['applicant_answer']
        pk = request.POST['pk']
        app = Application.objects.get(pk=pk)

        new_question = Question(question=question, applicant_answer=app_answer, actual_answer=company_answer, application=app)
        new_question.save()

        return JsonResponse({
            "question": new_question.question,
            "company_answer": new_question.actual_answer,
            "applicant_answer": new_question.applicant_answer,
            "success": True
        })

    return HttpResponse("failed to create a question!")

