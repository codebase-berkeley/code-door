from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from codedoor.models import Profile, Company, Question, Application, ApplicationComment, User
from django.core.paginator import Paginator
from django.core import serializers

import traceback
import ast
import json

def create_application(request,companypk):
    print("reached here")
    profilepk = request.user.profile.pk
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
            return HttpResponse("You did not fill out the form correctly")
        a = Application(company=Company.objects.get(pk=companypk), profile=Profile.objects.get(pk=profilepk), description=description, season=season, position=position, received_offer=received_offer, offer_details=offer_details, difficult=difficulty, year=year)
        a.save()
        # return redirect("codedoor:view_application", pk=a.id)
        return JsonResponse({"application": a})
    else:
        return HttpResponse("created an application")
        # return render(request, 'codedoor/createapplication.html', {"companypk": companypk})


def create_application_company(request):
    print("in create application company")
    profilepk = request.user.profile.pk
    companies = Company.objects.filter()
    if request.method == 'POST':
        print("inside the if")
        try:
            print(request.POST)
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
        a = Application(company=Company.objects.get(pk=companypk), profile=Profile.objects.get(pk=profilepk), description=description, season=season, position=position, received_offer=received_offer, offer_details=offer_details, difficult=difficulty, year=year)
        a.save()
        # return redirect("codedoor:view_application", pk=a.id)
        return JsonResponse({"a": serializers.serialize('json', Application.objects.filter(pk=a.pk)),
                             "c": serializers.serialize('json', Company.objects.filter(pk=a.company.pk)),
                             "p": serializers.serialize('json', Profile.objects.filter(pk=a.profile.pk)),
                             "u": serializers.serialize('json', User.objects.filter(pk=a.profile.user.pk))}, safe=False)
    else:
        return HttpResponse("created an application")
        # return render(request, 'codedoor/createapplicationcomp.html', {'companies' : companies})


def edit_application(request):
    print("Are we here ma dude")
    pk = request.POST['pk']
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
    else:
        return HttpResponse("couldn't edit the application")


def view_application(request, pk):
    a = get_object_or_404(Application, pk=pk)
    profile = get_object_or_404(Profile, id=a.profile.pk)
    questions = Question.objects.filter(application=pk).order_by("-pk")
    return render(request, "codedoor/viewapplication.html", {"a": a, "profile" : profile, "questions": questions})


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
        
    return render(request, "codedoor/listapplications.html", {"applications": applications, "page": applications_list})

def list_all_applications(request, pg=1):
    applications = Application.objects.order_by("-pk")
    paginator = Paginator(applications, 10) 
    page = request.GET.get('page', 1)
    try:
        applications_list = paginator.page(page)
    except PageNotAnInteger:
        applications_list = paginator.page(1)
    except EmptyPage:
        applications_list = paginator.page(paginator.num_pages)
        
    return render(request, "codedoor/listapplications.html", {"applications": applications, "page": applications_list})
    
def created_question(request):
    if request.method == "POST":

        question = request.POST['question']
        company_answer = request.POST['company_answer']
        app_answer = request.POST['applicant_answer']
        pk = request.POST['pk']
        app = Application.objects.get(pk=pk)

        new_question = Question(question=question, applicant_answer=app_answer, actual_answer=company_answer, application=app)
        new_question.save()

        return JsonResponse({"question": new_question.question, "company_answer": new_question.actual_answer, "applicant_answer": new_question.applicant_answer, "success": True})

    return HttpResponse("failed to create a question!")

