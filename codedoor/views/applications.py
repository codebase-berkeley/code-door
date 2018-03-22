from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from codedoor.models import Profile, Company, Question, Application
import traceback

def create_application(request):
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
        a = Application(company=Company.objects.get(pk=1), profile=Profile.objects.get(pk=1), description=description, season=season, position=position, received_offer=received_offer, offer_details=offer_details, difficult=difficulty, year=year)
        a.save()
        return redirect("codedoor:view_application", pk=a.id)
    else:
        return render(request, 'codedoor/createapplication.html')


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


#company, profiledescription = models.TextField()
    # year = models.IntegerField()
    #season = models.CharField(max_length=100, choices=SEASONS)
    #position = models.CharField(max_length=500)
    #received_offer = models.BooleanField()
    #offer_details = models.TextField(null=True, blank=True)
    #difficult = models.DecimalField(decimal_places=2, max_digits=10)

