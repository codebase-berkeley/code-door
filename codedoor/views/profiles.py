from api_keys_prod import s3_access_keys, slack_access_keys, absolute_url
import boto3
from codedoor.models import Profile
import datetime
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
import re
import requests
from requests.auth import HTTPBasicAuth
import sys
from urllib.parse import parse_qs

profile_pic_bucket = 'codedoor-profile-pictures'


def createprofile(request):
    if request.method == "GET":
        return render(request, 'codedoor/create_profile.html')
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
        return render(request, 'codedoor/finish_profile.html')
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
    return render(request, 'codedoor/view_profile.html', {"profile": profile})


@login_required
def editprofile(request, pk):
    if not request.user.profile.id == pk:
        return redirect("codedoor:viewprofile", pk=request.user.profile.id)  # where to redirect the wrong user trying to edit
    profile = get_object_or_404(Profile, pk=pk)
    user = profile.user
    if request.method == "GET":
        return render(request, 'codedoor/edit_profile.html', {"profile": profile})
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
    TEMPLATE_PATH = "codedoor/login.html"
    client_id = slack_access_keys["client_id"]
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
            return render(request, TEMPLATE_PATH, {"failed": True, "client_id": client_id})
    else:
        if not request.GET:
            return render(request, TEMPLATE_PATH, {"client_id": client_id})
        else:
            return render(request, TEMPLATE_PATH, {"next": request.GET['next'], "client_id": client_id})


def logout(request):
    auth_logout(request)
    return render(request, 'codedoor/logout.html')


def slack_info(request):
    """
    After a user logs into Slack, they are redirected to this view with several
    parameters added to the request if the Slack login was successful.

    See (https://api.slack.com/docs/oauth) for more.
    """
    params = slack_callback(request)

    if not params:
        # Authorization failed.
        return redirect("codedoor:login")

    # if user is already in database, return redirect(url)
    # else, if it's a new user, redirect to the finishprofile page for the user to input the rest of their info
    user = authenticate(params["user"]["email"])
    if user is None:
        first_name, last_name = params["user"]['name'].split(" ")
        return render(
            request,
            'codedoor/finish_profile.html',
            {
                "id": params['user']['email'],
                "first_name": first_name,
                "last_name": last_name,
                "email": params["user"]["email"],
                "pic": params["user"]['image_512']
            }
        )
    else:
        auth_login(request, user)
        return redirect("codedoor:viewprofile", pk=user.profile.id)


def slack_callback(request):
    client_id = slack_access_keys["client_id"]
    client_secret = slack_access_keys["client_secret"]

    if request.method == 'GET':
        code = request.GET.get('code')
        get_token_url = "https://slack.com/api/oauth.access?client_id={}&client_secret={}&code={}".format(client_id,
                                                                                                          client_secret,
                                                                                                          code)
        r = requests.post(get_token_url,
                auth=HTTPBasicAuth(client_id, client_secret),
                headers={"content-type": "application/x-www-form-urlencoded"},
                params={"code": code, "grant_type": "authorization_code"})

        try:
            access_token = r.json()['access_token']

            get_activity_url = "https://slack.com/api/users.identity"
            r = requests.post(get_activity_url,
                              headers={"Authorization": "Bearer " + access_token})
            return r.json()
        except Exception as e:
            # Authorization failed.
            return None

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

@csrf_exempt
def slackbot_callback(request):
    """
    Slack callback for a codebucks bot event.
    :param request:
    :return:
    """
    # TODO: Verify that the request is coming from slack by checking the verification token in the request
    if request.content_type == "application/json":
        body = json.loads(request.body.decode("utf-8"))
        print("Slackbot messaged received:{}".format(body))
        sys.stdout.flush()
        if "event" in body:
            e = body["event"]
            if e["type"] in ["app_mention", "message"]:
                if "subtype" in e and e["subtype"] == "bot_message":
                    return HttpResponse(200)
                channel = e["channel"]
                r = requests.post(
                    "https://slack.com/api/chat.postMessage",
                    headers={
                        "content-type": "application/x-www-form-urlencoded",
                        "Authorization": "Bearer {}".format(slack_access_keys["slackbot_token"])
                    },
                    params={
                        "text": "Hello!",
                        "channel": channel
                    }
                )
        elif "challenge" in body:
            return JsonResponse({"challenge": body["challenge"]})
    elif request.content_type == "application/x-www-form-urlencoded":
        # the request is a slash command, not a message to the bot.
        command_qs = parse_qs(request.body.decode("utf-8"))
        print(command_qs)
        user_id = command_qs["user_id"][0]
        if command_qs["command"][0] == "/send":
            match = re.match("<@([\w+|]+)>\s+(\d+)", command_qs["text"][0])
            if match is None:
                # return help message
                return HttpResponse("I don't recognize that command. Try `/codebank` to see a list of commands!")
            else:
                recipient_id = match.group(1).split("|")[0]
                amount = int(match.group(2))
                print("Attempting to send {} from {} to {}".format(amount, user_id, recipient_id))
                success = send_codebucks(user_id, recipient_id, amount)
                if success:
                    return HttpResponse("You sent {} codebucks to <@{}>".format(amount, recipient_id))
                return HttpResponse("It looks like that transaction is invalid. Make sure you have enough codebucks and "
                                    "that your recipient has a codebank account!")
        elif command_qs["command"][0] == "/codebank":
            user_profile = get_profile(user_id)
            top_profiles = Profile.objects.all().order_by('-codebucks')[:3]
            leaderboard_text = "The top 3 codebucks accounts are:"
            for i in range(len(top_profiles)):
                p = top_profiles[i]
                leaderboard_text += "\n{}. **{}** ({} CB)".format(i+1, p.user.get_full_name(), p.codebucks)
            return JsonResponse({
                "text": "Welcome to Codebank, {}! Your balance is {} codebucks.".format(
                    user_profile.user.first_name, user_profile.codebucks),
                "attachments": [
                    {
                        "text": "Type `/send [@user] [amount]` to send some codebucks to a friend."
                    },
                    {
                        "text": leaderboard_text
                    }
                ]
            })
    return HttpResponse(200)

def send_codebucks(sender_uid, recipient_uid, amount):
    """
    :param sender_uid: Slack UID of the sender.
    :param recipient_uid: Slack UID of the recipient.
    :param amount: Positive integer amount to send.
    :return: True if the transaction completed successfully, else False
    """
    sender = get_profile(sender_uid)
    recipient = get_profile(recipient_uid)
    if sender and recipient and sender != recipient:
        if sender.codebucks < amount:
            return False
        with transaction.atomic():
            sender.codebucks -= amount
            recipient.codebucks += amount
            sender.save()
            recipient.save()
        return True
    return False

def get_profile(slack_uid):
    r = requests.post(
        "https://slack.com/api/users.info",
        headers={
            "content-type": "application/x-www-form-urlencoded",
        },
        params={
            "token": slack_access_keys["slackbot_token"],
            "user": slack_uid
        }
    )
    data = r.json()
    try:
        email = data["user"]["profile"]["email"]
        profile = Profile.objects.get(user=User.objects.get(email=email))
        return profile
    except Exception:
        return None
