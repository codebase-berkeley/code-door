from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from codedoor.models import Profile, Company, Question, Application
from django.core.paginator import Paginator
import traceback

def create_application(request,companypk,profilepk):
    if request.method == 'POST':
        print(companypk,profilepk, "HERREEEE")
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
        return redirect("codedoor:view_application", pk=a.id)
    else:
        return render(request, 'codedoor/createapplication.html', {"companypk": companypk, "profilepk": profilepk})


def edit_application(request, pk):
    a = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        try:
            a.description = request.POST['description']
            a.season = request.POST['season']
            a.position = request.POST['position']
            received_offer = request.POST['received_offer']
            a.year = request.POST['year']
            if(received_offer == "on"):
                a.received_offer = True
            else:
                a.received_offer = False
            a.offer_details = request.POST['offer_details']
            a.difficulty = request.POST['difficulty']
        except Exception as e:
            traceback.print_exc()
            return HttpResponse("You did not fill out the form correctly")
        a.save()
        return redirect("codedoor:view_application", pk=a.id)
    else:
        return render(request, 'codedoor/editapplication.html',
                      {
                          "description": a.description,
                          "season": a.season,
                          "position": a.position,
                          "received_offer": a.received_offer,
                          "year": a.year,
                          "offer_details": a.offer_details,
                          "difficulty": a.difficult,
                          "pk": pk,
                          "link": "/codedoor/editapplication/" + str(pk)
                      })

# 
def view_application(request, pk):
    a = get_object_or_404(Application, pk=pk)
    return render(request, "codedoor/viewapplication.html", {"a": a})

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

