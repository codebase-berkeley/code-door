from api_keys_prod import s3_access_keys, slack_access_keys, absolute_url
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from codedoor.models import Profile
import json
import random
import re
import requests
from requests.auth import HTTPBasicAuth
import sys
from urllib.parse import parse_qs

# Create your views here.

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
                if amount < 100:
                    return HttpResponse("The minimum transaction is 100 codebucks.")
                success = send_codebucks(user_id, recipient_id, amount)
                if success:
                    r = requests.post(
                        "https://slack.com/api/chat.postMessage",
                        headers={
                            "content-type": "application/x-www-form-urlencoded",
                            "Authorization": "Bearer {}".format(slack_access_keys["slackbot_token"])
                        },
                        params={
                            "text": "<@{}> sent {} codebucks to <@{}>".format(user_id, amount, recipient_id),
                            "channel": "CGBHVU06T"
                        }
                    )
                    return HttpResponse("You sent {} codebucks to <@{}>".format(amount, recipient_id))
                return HttpResponse("It looks like that transaction is invalid. Make sure you have enough codebucks and "
                                    "that your recipient has a codebank account!")
        elif command_qs["command"][0] == "/codebank":
            user_profile = get_profile(user_id)
            if user_profile is None:
                return HttpResponse("It looks like you don't have a Codebank account yet. "
                                    "Visit https://codedoor-prod.herokuapp.com to create one!")
            top_profiles = Profile.objects.all().order_by('-codebucks')[:3]
            leaderboard_text = "The top 3 codebucks accounts are:"
            for i in range(len(top_profiles)):
                p = top_profiles[i]
                leaderboard_text += "\n{}. {} ({} CB)".format(i+1, p.user.get_full_name(), p.codebucks)
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
        elif command_qs["command"][0] == "/coinflip":
            match = re.match("(\d+)", command_qs["text"][0])
            if match is None:
                return HttpResponse("Command is /coinflip [amount]. Wagers [amount] on a fair coin flip.")
            else:
                profile = get_profile(user_id)
                amount = int(match.group(1))
                if profile.codebucks < amount:
                    return HttpResponse("You don't have enough codebucks.")
                elif amount < 100:
                    return HttpResponse("The gambling committee requires a minimum wager of at least 100 codebucks.")
                if (random.random() < 0.49):
                    amount = amount * -1
                with transaction.atomic():
                    profile.codebucks += amount
                    profile.save()
                if amount < 0:
                    msg = "lost"
                else:
                    msg = "gained"

                r = requests.post(
                    "https://slack.com/api/chat.postMessage",
                    headers={
                        "content-type": "application/x-www-form-urlencoded",
                        "Authorization": "Bearer {}".format(slack_access_keys["slackbot_token"])
                    },
                    params={
                        "text": "<@{}> has {} {} codebucks.".format(user_id, msg, abs(amount)),
                        "channel": "CGBHVU06T"
                    }
                )
                return HttpResponse("<@{}> has {} {} codebucks.".format(user_id, msg, abs(amount)))
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
