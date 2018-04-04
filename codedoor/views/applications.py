from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from codedoor.models import Profile, Company, Question, Application
<<<<<<< HEAD
from django.core.paginator import Paginator
import traceback

def create_application(request,companypk,profilepk):
=======
import traceback

def create_application(request):
>>>>>>> c16ebfbafb01656e730eab4554447671c436eec6
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
<<<<<<< HEAD
        a = Application(company=Company.objects.get(pk=companypk), profile=Profile.objects.get(pk=profilepk), description=description, season=season, position=position, received_offer=received_offer, offer_details=offer_details, difficult=difficulty, year=year)
        a.save()
        return redirect("codedoor:view_application", pk=a.id)
    else:
        return render(request, 'codedoor/createapplication.html', {"companypk": companypk, "profilepk": profilepk})
=======
        a = Application(company=Company.objects.get(pk=1), profile=Profile.objects.get(pk=1), description=description, season=season, position=position, received_offer=received_offer, offer_details=offer_details, difficult=difficulty, year=year)
        a.save()
        return redirect("codedoor:view_application", pk=a.id)
    else:
        return render(request, 'codedoor/createapplication.html')
>>>>>>> c16ebfbafb01656e730eab4554447671c436eec6


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

<<<<<<< HEAD
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
=======

#company, profiledescription = models.TextField()
    # year = models.IntegerField()
    #season = models.CharField(max_length=100, choices=SEASONS)
    #position = models.CharField(max_length=500)
    #received_offer = models.BooleanField()
    #offer_details = models.TextField(null=True, blank=True)
    #difficult = models.DecimalField(decimal_places=2, max_digits=10)
>>>>>>> c16ebfbafb01656e730eab4554447671c436eec6

