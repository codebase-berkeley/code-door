from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile


def hello(request):
    return render(request, 'codedoor/hello.html', {'name': 'Brian'})


def createprofile(request):
    if request.method == "GET":
        return render(request, 'codedoor/createprofile.html')
    else:
        input_name = request.POST['name']
        # input_profile_pic = request.POST['profile_pic']
        input_graduation_year = request.POST['graduation_year']
        input_current_job = request.POST['current_job']
        input_linkedin = request.POST['linkedin']
        # input_resume = request.POST['resume']
        profile = Profile(name=input_name,
                          graduation_year=input_graduation_year, current_job=input_current_job,
                          linkedin=input_linkedin)
        profile.save()
        return HttpResponse("Profile successfully created!")


def viewprofile(request, pk):
    profile = Profile.objects.get(id=pk)
    return render(request, 'codedoor/viewprofile.html', {"profile": profile})


def editprofile(request, pk):
    profile = Profile.objects.get(id=pk)
    if request.method == "GET":
        return render(request, 'codedoor/editprofile.html', {"profile": profile})
    else:
        profile.name = request.POST['name']
        # input_profile_pic = request.POST['profile_pic']
        profile.graduation_year = request.POST['graduation_year']
        profile.current_job = request.POST['current_job']
        profile.linkedin = request.POST['linkedin']
        # input_resume = request.POST['resume']
        profile.save()
        return HttpResponse("Profile successfully updated.")


def edit(request):
    profile = Profile.objects.get(pk=int(request.POST['pk']))
    profile.name = request.POST['name']
    # input_profile_pic = request.POST['profile_pic']
    profile.graduation_year = request.POST['graduation_year']
    profile.current_job = request.POST['current_job']
    profile.linkedin = request.POST['linkedin']
    # input_resume = request.POST['resume']
    profile.save()
    return HttpResponse("Profile successfully updated.")
