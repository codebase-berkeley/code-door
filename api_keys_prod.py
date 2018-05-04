import os

def config(var):
    return os.environ[var]

if config("production"):
    s3_access_keys = {
        "id": config("s3_id"),
        "secret": config("s3_secret")
    }

    slack_access_keys = {
        "client_id" : config("slack_id"),
        "client_secret": config("slack_secret")
    }

    absolute_url = config("absolute_url")
else:
    from api_keys import s3_access_keys as s3, slack_access_keys as slack, absolute_url as url
    s3_access_keys = s3
    slack_access_keys = slack
    absolute_url = url
