from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from codedoor.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import requests
from requests.auth import HTTPBasicAuth

import urllib
import base64


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
    if not request.user.profile.id == pk:
        return redirect("codedoor:viewprofile", pk=pk)  # where to redirect the wrong user trying to edit
    profile = get_object_or_404(Profile, pk=pk)
    user = profile.user
    if request.method == "GET":
        return render(request, 'codedoor/editprofile.html', {"profile": profile})
    else:
        try:
            profile.user.email = request.POST['email']
            profile.user.first_name = request.POST['first_name']
            profile.user.last_name = request.POST['last_name']
            profile.user.username = request.POST['username']
            # profile.user.password = request.POST['password']
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
        user.save()
        profile.save()
        return redirect("codedoor:viewprofile", pk=pk)


def login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        user = authenticate(request, username=uname, password=pwd)

        if user is not None:
            auth_login(request, user)
            if request.POST.get('next'):
                return redirect(request.POST.get('next'))
            else:
                return redirect("codedoor:viewprofile", pk=user.profile.id)  # Eventually redirect to home page
        else:
            return render(request, "codedoor/login.html", {"failed": True})
    else:
        if not request.GET:
            return render(request, 'codedoor/login.html')
        else:
            return render(request, 'codedoor/login.html', {"next": request.GET['next']})


def logout(request):
    auth_logout(request)
    return render(request, 'codedoor/logout.html')


def slack_info(request):
    params = slack_callback(request)
    url = "https://slack.com/oauth/authorize?" + urllib.parse.urlencode(params)
    return redirect(url)


def slack_callback(request):
    client_id = "44822465026.334128598816"
    client_secret = "7387eabf2e73804cf8492e6025c89326"

    if request.method == 'GET':
        code = request.GET.get('code')
        get_token_url = "https://slack.com/api/oauth.access?client_id={}&client_secret={}&code={}".format(client_id, client_secret, code)
        r = requests.post(get_token_url,
                          auth=HTTPBasicAuth(client_id, client_secret),
                          headers={"content-type": "application/x-www-form-urlencoded"},
                          params={"code": code, "grant_type": "authorization_code",
                                  "redirect_uri": "http://localhost:8000/codedoor/slack_callback"})
        access_token = r.json()['access_token']

        get_activity_url = "https://slack.com/api/users.identity"
        r = requests.post(get_activity_url,
                          headers={"Authorization": "Bearer " + access_token})

        return JsonResponse(r.json())

