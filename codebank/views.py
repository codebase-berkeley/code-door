from api_keys_prod import s3_access_keys, slack_access_keys, absolute_url
from codebank.utils import get_email, send_codebucks, coinflip, TransactionError
from codedoor.models import Profile
from datetime import datetime
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
import hmac
import json
import random
import re
import requests
from slackclient import SlackClient
import sys
from urllib.parse import parse_qs


# Create your views here.

slack = SlackClient(slack_access_keys["slackbot_token"] if "slackbot_token" in slack_access_keys else "")

def verify_slack_request(request):
    print(request.META)
    slack_signing_secret = slack_access_keys['signing_secret']
    request_body = request.body.decode("utf-8")
    timestamp = request.META['HTTP_X_SLACK_REQUEST_TIMESTAMP']
    if abs(datetime.now().timestamp() - float(timestamp)) > 60.0 * 5.0:
        return False # replay attack
    sig_basestring = str.encode('v0:' + timestamp + ':' + request_body)
    my_signature = 'v0=' + hmac.new(str.encode(slack_signing_secret), sig_basestring, hashlib.sha256).hexdigest()
    slack_signature = request.META['HTTP_X_SLACK_SIGNATURE']
    if not hmac.compare_digest(my_signature, slack_signature):
        return False # request didn't originate from slack
    return True


@csrf_exempt
def slackbot_callback(request):
    """
    Slack callback for a codebucks bot event.
    :param request:
    :return:
    """
    # Verify that the request is coming from slack by checking the verification token in the request
    if not verify_slack_request(request):
        return

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
        user_id = command_qs["user_id"][0]
        if command_qs["command"][0] == "/send":
            match = re.match("<@([\w+|]+)>\s+(\d+)(\s+.*)?", command_qs["text"][0])
            if match is None:
                # return help message
                return HttpResponse("I don't recognize that command. Try `/codebank` to see a list of commands!")
            else:
                recipient_id = match.group(1).split("|")[0]
                amount = int(match.group(2))
                note = match.group(3).strip() if match.group(3) else ""
                print("Attempting to send {} from {} to {}".format(amount, user_id, recipient_id))
                try:
                    send_codebucks(get_email(user_id), get_email(recipient_id), amount)
                    blocks = [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "<@{}> sent {} codebucks to <@{}>".format(user_id, amount, recipient_id)
                            }
                        }
                    ]
                    if note != "":
                        blocks.append({
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "> {}".format(note)
                            }
                        })
                    slack.api_call(
                        "chat.postMessage",
                        channel="CGBHVU06T",
                        blocks=blocks
                    )
                    return HttpResponse("You sent {} codebucks to <@{}>".format(amount, recipient_id))
                except TransactionError as e:
                    return HttpResponse(e.msg)
        elif command_qs["command"][0] == "/codebank":
            user_profile = Profile.objects.get(user=User.objects.get(email=get_email(user_id)))
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
                        "text": "Type `/send [@user] [amount] [note]` to send some codebucks to a friend."
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
                amount = int(match.group(1))
                try:
                    amount = coinflip(get_email(user_id), amount)
                    if amount < 0:
                        msg = "lost"
                    else:
                        msg = "gained"
                    slack.api_call(
                        "chat.postMessage",
                        channel="CGBHVU06T",
                        text="<@{}> has {} {} codebucks.".format(user_id, msg, abs(amount))
                    )
                    return HttpResponse("<@{}> has {} {} codebucks.".format(user_id, msg, abs(amount)))
                except TransactionError as e:
                    return HttpResponse(e.msg)
    return HttpResponse(200)
