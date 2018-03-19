from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from codedoor.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def createprofile(request):
    if request.method == "GET":
        return render(request, 'codedoor/createprofile.html')
    else:
        try:
            input_username = request.POST['username']
            input_password = request.POST['password']
            input_email = request.POST['email']
            input_first_name = request.POST['first_name']
            input_last_name = request.POST['last_name']
            # input_profile_pic = request.POST['profile_pic']
            input_graduation_year = request.POST['graduation_year']
            input_current_job = request.POST['current_job']
            input_linkedin = request.POST['linkedin']
            if "http://" not in input_linkedin and "https://" not in input_linkedin:
                input_linkedin = "http://" + input_linkedin
            # input_resume = request.POST['resume']
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly!") # TODO: message displayed on form

        user = User.objects.create_user(username=input_username, password=input_password, email=input_email,
                                            first_name=input_first_name, last_name=input_last_name)
        user.save()
        profile = Profile(user=user, graduation_year=input_graduation_year, current_job=input_current_job,
                          linkedin=input_linkedin)
        profile.save()
        return redirect("codedoor:viewprofile", pk=profile.id)


@login_required
def viewprofile(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    return render(request, 'codedoor/viewprofile.html', {"profile": profile})


@login_required
def editprofile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == "GET":
        return render(request, 'codedoor/editprofile.html', {"profile": profile})
    else:
        try:
            profile.User.email = request.POST['email']
            profile.User.first_name = request.POST['first_name']
            profile.User.last_name = request.POST['last_name']
            # profile.profile_pic = request.POST['profile_pic']
            profile.graduation_year = request.POST['graduation_year']
            profile.current_job = request.POST['current_job']
            print(profile.current_job)
            input_linkedin = request.POST['linkedin']
            if "http://" not in input_linkedin and "https://" not in input_linkedin:
                input_linkedin = "http://" + input_linkedin
            profile.linkedin = input_linkedin
            # profile.resume = request.POST['resume']
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly!")

        profile.save()
        return redirect("codedoor:viewprofile", pk=pk)


def login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        user = authenticate(request, username=uname, password=pwd)

        if user is not None:
            auth_login(request, user)
            return viewprofile(request, pk)
        else:
            return render(request, "posts/login.html")
    else:
        return render(request, "posts/login.html")


def logout(request):
    auth_logout(request)
    return render(request, "posts/logout.html")