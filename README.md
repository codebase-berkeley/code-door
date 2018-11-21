# CodeDoor

For testing purposes, please setup the superuser to use:

* username: `development`
* password: `codebase`

The production server does **not** have a superuser configured.

## Installation

See the [first time setup guide](https://github.com/codebase-berkeley-mentored-project-sp18/Guides/blob/master/SetupGuide.pdf) for a full walkthrough.

1. Clone this repository and cd into the root directory.
2. Create a virtual environment with `python3 -m venv env`.
3. Activate the virtual environment with `source env/bin/activate`.
4. Install the project dependencies with `pip install -r requirements.txt`.
5. Start a Postgres server with `service postgresql start`.
6. Build migration scripts with `python manage.py makemigrations codedoor`.
7. Run `python manage.py migrate` to create the CodeDoor database and schema in the postgres DB backend.
8. Create a file called `api_keys.py` in the root directory with the correct credentials (see: "Developing Locally" for local credentials).
9. Run `python manage.py runserver` to run the server.
10. Go to `localhost:8000` to see it in action!

## Overview

CodeDoor runs on top of the [Django web framework](https://www.djangoproject.com/)
and uses Postgres as a backing database. The Slack OAuth API is used for login;
our Slack developer account contains keys as well as the callback URL,
which is set to point to our production server.

For static files like profile pictures, we currently use Amazon S3 as a backing store.
The production server is deployed on Heroku at (http://codedoordev.herokuapp.com).
Please message Brian or Andrew on Slack for more details about credentials or deployment.

[The original CodeDoor design can be viewed on Figma](https://www.figma.com/file/LXlfHxd8cLK4RFJ7yHP0tuFI/Codor-Prototype).

## Contributing

There is a lot to fix! If you would like to contribute, please work using feature branches forked from `master`.
Suggested workflow:

1. Fork a branch from `master`.
2. Make and commit your changes. There is no style guide currently.
3. Submit a pull request on GitHub from your branch into `master`, putting Andrew Chan as your reviewer.
4. Andrew will review your change and merge it.

Please message Andrew on Slack if you have any questions about the contribution process.

### Developing Locally

You can run a local instance of CodeDoor by following the steps in the Installation section.
**You'll need access to the Slack credentials for the local-only Slack app - look in the slack channel or message Andrew for more.**
Note that these credentials are different from the production server's credentials,
which are associated with a Slack app that redirects to the production server.

You'll also need our **Amazon S3 credentials**, which can be found in the slack channel. Once you have these credentials,
create a file in the project root directory called `api_keys.py` with the following:

```python
s3_access_keys = {
    "id": "<S3_ID>",
    "secret": "<S3_SECRET>"
}

slack_access_keys = {
    "client_id" : "<SLACK_ID>",
    "client_secret" : "<SLACK_SECRET>"
}

absolute_url = "http://localhost:8000"
```

You are now ready to run a local instance of CodeDoor.

### Deploying to Production

Our production instance runs on Heroku and uses different credentials than the local instances; these are passed to the program
using environment variables. The following variables need to be set:

```
absolute_url=https://codedoordev.herokuapp.com/
DATABASE_URL=postgres://<DATABASE_USER>:<DATABASE_PASSWORD>@<DATABASE_HOST>
production=True
s3_id=<S3_ID>
s3_secret=<S3_SECRET>
slack_id=<SLACK_ID>
slack_secret=<SLACK_SECRET>
```

Automatic deploys have not been set up.
