from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from codedoor.models import Profile, Company, Question, Application

def create_application(request):
	if request.method == 'POST':
        try:
            description = request.POST['description']
            season = request.POST['season']
            position = request.POST['position']
            receieved_offer = request.POST['recieved offer']
            offer_details = request.POST['offer detials']
            difficulty = request.POST['difficulty']
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly")

        a = Application(company=Company.objects.get(pk=1), profile=Profile.objects.get(pk=1), season=season, position=position, received_offer=received_offer, offer_details=offer_details, difficult=difficulty)
        a.save()
        return redirect("codedoor:view_application", pk=q.id)
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

