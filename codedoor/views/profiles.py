from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from codedoor.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import requests
from requests.auth import HTTPBasicAuth
import datetime
import boto3
from api_keys_prod import s3_access_keys
from api_keys_prod import slack_access_keys
from api_keys_prod import absolute_url

profile_pic_bucket = 'codedoor-profile-pictures'


def createprofile(request):
    if request.method == "GET":
        return render(request, 'codedoor/createprofile.html')
    else:
        try:
            input_username = request.POST['email']
            input_password = request.POST['password']
            input_email = request.POST['email']
            input_first_name = request.POST['first_name']
            input_last_name = request.POST['last_name']
            input_profile_pic = request.FILES['profile_pic'].read()
            input_graduation_year = request.POST['graduation_year']
            input_current_job = request.POST['current_job']
            input_linkedin = request.POST['linkedin']
            if "http://" not in input_linkedin and "https://" not in input_linkedin and input_linkedin:
                input_linkedin = "http://" + input_linkedin
            # input_resume = request.POST['resume']
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly!")  # TODO: message displayed on form

        user = User.objects.create_user(username=input_username, password=input_password, email=input_email,
                                        first_name=input_first_name, last_name=input_last_name)
        profile = Profile(user=user, graduation_year=input_graduation_year,
                          current_job=input_current_job, linkedin=input_linkedin)

        user.save()
        profile.save()
        upload_picture(input_profile_pic, profile)
        profile.save()
        user = authenticate(request, username=input_username, password=input_password)
        auth_login(request, user)
        return redirect("codedoor:viewprofile", pk=profile.id)


def finishprofile(request):
    if request.method == "GET":
        return render(request, 'codedoor/finishprofile.html')
    else:
        try:
            # not sure how to extract these the info commented before from the slack API to save as a user
            input_id = request.POST['email']
            input_email = request.POST['email']
            input_first_name = request.POST['first_name']
            input_last_name = request.POST['last_name']
            input_profile_pic = request.FILES['profile_pic'].read()
            input_graduation_year = request.POST['graduation_year']
            input_current_job = request.POST['current_job']
            input_linkedin = request.POST['linkedin']
            if "http://" not in input_linkedin and "https://" not in input_linkedin and input_linkedin:
                input_linkedin = "http://" + input_linkedin
            # input_resume = request.POST['resume']

        except Exception as e:
            return HttpResponse("You did not fill out the form correctly!")  # TODO: message displayed on form

        user = User.objects.create_user(username=input_id, password=" ", email=input_email,
                                        first_name=input_first_name, last_name=input_last_name)
        profile = Profile(user=user, graduation_year=input_graduation_year,
                          current_job=input_current_job, linkedin=input_linkedin)
        user.save()
        profile.save()
        upload_picture(input_profile_pic, profile)
        profile.save()
        user = authenticate(request, username=input_id)
        auth_login(request, user)
        return redirect("codedoor:viewprofile", pk=profile.id)  # Eventually redirect to home page


@login_required
def viewprofile(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    return render(request, 'codedoor/viewprofile.html', {"profile": profile})


@login_required
def editprofile(request, pk):
    if not request.user.profile.id == pk:
        return redirect("codedoor:viewprofile", pk=request.user.profile.id)  # where to redirect the wrong user trying to edit
    profile = get_object_or_404(Profile, pk=pk)
    user = profile.user
    if request.method == "GET":
        return render(request, 'codedoor/editprofile.html', {"profile": profile})
    else:
        try:
            input_profile_pic = False
            profile.user.first_name = request.POST['first_name']
            profile.user.last_name = request.POST['last_name']
            try:
                input_profile_pic = request.FILES['profile_pic'].read()
            except Exception as e:
                pass
            profile.graduation_year = request.POST['graduation_year']
            profile.current_job = request.POST['current_job']
            input_linkedin = request.POST['linkedin']
            if "http://" not in input_linkedin and "https://" not in input_linkedin and input_linkedin:
                input_linkedin = "http://" + input_linkedin
            profile.linkedin = input_linkedin
        except Exception as e:
            return HttpResponse("You did not fill out the form correctly!")
        if input_profile_pic:
            upload_picture(input_profile_pic, profile)
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
                return redirect("codedoor:home")
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
    return params
    # insert if/else statement
    # if user is already in database, return redirect(url)
    # else, if it's a new user, redirect to the finishprofile page for the user to input the rest of their info
    user = authenticate(params["user"]["email"])
    if user is None:
        print("Profile is None")
        first_name, last_name = params["user"]['name'].split(" ")
        return render(request, 'codedoor/finishprofile.html', {"id": params['user']['email'], "first_name": first_name, "last_name": last_name, "email": params["user"]["email"], "pic": params["user"]['image_512']})
    else:
        print("nani the fuck")
        auth_login(request, user)
        return redirect("codedoor:viewprofile", pk=user.profile.id)


def slack_callback(request):
    print("IN CALLBACK")
    client_id = slack_access_keys["client_id"]
    client_secret = slack_access_keys["client_secret"]

    if request.method == 'GET':
        code = request.GET.get('code')
        print("Code", code)
        get_token_url = "https://slack.com/api/oauth.access?client_id={}&client_secret={}&code={}".format(client_id,
                                                                                                          client_secret,
                                                                                                          code)
        r = requests.post(get_token_url,
                          auth=HTTPBasicAuth(client_id, client_secret),
                          headers={"content-type": "application/x-www-form-urlencoded"},
                          params={"code": code, "grant_type": "authorization_code"})
        
        print(r.json())
        try:
            access_token = r.json()['access_token']
        except:
            return JsonResponse(r.json())

        get_activity_url = "https://slack.com/api/users.identity"
        r = requests.post(get_activity_url,
                          headers={"Authorization": "Bearer " + access_token})
        
        return r.json()


def upload_picture(input_profile_pic, profile):
    s3 = boto3.resource('s3', aws_access_key_id=s3_access_keys["id"],
                        aws_secret_access_key=s3_access_keys["secret"])
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d:%H:%M:%S')
    s3.Bucket(profile_pic_bucket).put_object(Key="%s/%s" % (profile.id, timestamp),
                                             Body=input_profile_pic, ACL='public-read')
    url = "https://s3-us-west-1.amazonaws.com/" + profile_pic_bucket + "/" + str(profile.id) + "/" \
          + timestamp
    profile.profile_pic = url
    profile.save()
