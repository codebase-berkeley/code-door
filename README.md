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
5. Start a Postgres server with `service postgres start`.
6. Build migration scripts with `python manage.py makemigrations codedoor`.
7. Run `python manage.py migrate` to create the CodeDoor database and schema in the postgres DB backend.
8. Run `python manage.py runserver` to run the server.
9. Go to `localhost:8000` to see it in action!

## Overview

CodeDoor runs on top of the [Django web framework](https://www.djangoproject.com/) 
and uses Postgres as a backing database. The Slack OAuth API is used for login;
our Slack developer account contains keys as well as the callback URL, 
which is set to point to our production server.

For static files like profile pictures, we currently use Amazon S3 as a backing store.
The production server is deployed on Heroku at (http://codedoordev.herokuapp.com).
Please message Brian or Andrew on Slack for more details about credentials or deployment.

