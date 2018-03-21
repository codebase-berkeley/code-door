from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from codedoor.models import Profile, Company, Question, Application
import traceback

def create_application(request):
    if request.method == 'POST':
        try:
            print("ERROR HERE")
            description = request.POST['description']
            season = request.POST['season']
            position = request.POST['position']
            received_offer = request.POST['received_offer']
            year = request.POST['year']
            if(received_offer == "on"):
                print("in the if")
                received_offer = True
            else:
                print("in the else")
                received_offer = False
            offer_details = request.POST['offer_details']
            difficulty = request.POST['difficulty']
        except Exception as e:
            traceback.print_exc()
            return HttpResponse("You did not fill out the form correctly")
        # print(Company.objects.get(pk=1), Profile.objects.get(pk=1), description, season, position, received_offer, offer_details, difficulty)
        a = Application(company=Company.objects.get(pk=1), profile=Profile.objects.get(pk=1), description=description, season=season, position=position, received_offer=received_offer, offer_details=offer_details, difficult=difficulty, year=year)
        a.save()
        return redirect("codedoor:view_application", pk=a.id)
    else:
        return render(request, 'codedoor/createapplication.html')

# 
#def edit_application(request):


#company, profiledescription = models.TextField()
    # year = models.IntegerField()
    #season = models.CharField(max_length=100, choices=SEASONS)
    #position = models.CharField(max_length=500)
    #received_offer = models.BooleanField()
    #offer_details = models.TextField(null=True, blank=True)
    #difficult = models.DecimalField(decimal_places=2, max_digits=10)

