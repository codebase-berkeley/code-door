from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.urls import path

import codedoor.views as views

urlpatterns = [
    path('createprofile', views.createprofile, name='createprofile'),
    path('slackbot_callback', views.slackbot_callback, name='slackbot_callback'),
    path('editprofile/<int:pk>', views.editprofile, name='editprofile'),
    path('finishprofile/', views.finishprofile, name='finishprofile'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('slack_callback/', views.slack_callback, name='slack_callback'),
    path('slack_info/', views.slack_info, name='slack_info'),
    path('viewprofile/<int:pk>', views.viewprofile, name='viewprofile'),
]
