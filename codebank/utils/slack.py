from api_keys_prod import s3_access_keys, slack_access_keys, absolute_url
from codedoor.models import Profile
from django.contrib.auth.models import User
import requests

def get_profile(slack_uid, lock_row=False):
    """
    Selects a profile based on slack UID.
    :param slack_uid: The string slack UID.
    :param lock_row: If True, then lock the row until it has been updated and saved.
    :return: Corresponding profile or None.
    """
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
        if lock_row:
            return Profile.objects.select_for_update().get(user=User.objects.get(email=email))
        return Profile.objects.get(user=User.objects.get(email=email))
    except Exception:
        return None