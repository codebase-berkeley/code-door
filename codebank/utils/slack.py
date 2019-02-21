from api_keys_prod import s3_access_keys, slack_access_keys, absolute_url
from codedoor.models import Profile
import requests

def get_email(slack_uid):
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
        return data["user"]["profile"]["email"]
    except Exception as e:
        print(e)
        return None