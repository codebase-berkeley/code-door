from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Profile


def hello(request):
    return render(request, 'codedoor/hello.html', {'name': 'Brian'})


def createprofile(request):
    if request.method == "GET":
        return render(request, 'codedoor/createprofile.html')
    else:
        try:
            input_name = request.POST['name']
            # input_profile_pic = request.POST['profile_pic']
            input_graduation_year = request.POST['graduation_year']
            input_current_job = request.POST['current_job']
            input_linkedin = request.POST['linkedin']
            if "http://" not in input_linkedin and "https://" not in input_linkedin:
                input_linkedin = "http://" + input_linkedin
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly!") # TODO: message displayed on form

        # input_resume = request.POST['resume']
        profile = Profile(name=input_name,
                          graduation_year=input_graduation_year, current_job=input_current_job,
                          linkedin=input_linkedin)
        profile.save()
        return redirect("codedoor:viewprofile", pk=profile.id)


def viewprofile(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    return render(request, 'codedoor/viewprofile.html', {"profile": profile})


def editprofile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == "GET":
        return render(request, 'codedoor/editprofile.html', {"profile": profile})
    else:
        try:
            profile.name = request.POST['name']
            # input_profile_pic = request.POST['profile_pic']
            profile.graduation_year = request.POST['graduation_year']
            profile.current_job = request.POST['current_job']
            print(profile.current_job)
            input_linkedin = request.POST['linkedin']
            if "http://" not in input_linkedin and "https://" not in input_linkedin:
                input_linkedin = "http://" + input_linkedin
            profile.linkedin = input_linkedin
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly!")

        # input_resume = request.POST['resume']
        profile.save()
        return redirect("codedoor:viewprofile", pk=pk)

