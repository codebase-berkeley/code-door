from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.urls import path

import codebank.views as views

urlpatterns = [
    path('slackbot_callback', views.slackbot_callback, name='slackbot_callback'),
]
