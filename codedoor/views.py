from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile

def hello(request):
	return render(request, 'codedoor/hello.html', {'name': 'Brian'})

def createprofile(request):
    render(request, 'codedoor/createprofile.html')
    input_name = request.POST['name']
    input_profile_pic = request.POST['profile_pic']
    input_graduation_year = request.POST['graduation_year']
    input_current_job = request.POST['current_job']
    input_linkedin = request.POST['linkedin']
    input_resume = request.POST['resume']
    profile = Profile(name = input_name, profile_pic = input_profile_pic,
					  graduation_year = input_graduation_year, current_job = input_current_job,
					  linkedin = input_linkedin, resume = input_resume)
    profile.save()
    return HttpResponse("Profile successfully created!")
# can redirect to a page with this message decorated with CSS & options to
# view/edit profile or go back to dashboard
# or can redirect to view profile page


def viewprofile(request):
    return render(request, 'codedoor/viewprofile.html')


def editprofile(request):
    return render(request, 'codedoor/editprofile.html')

