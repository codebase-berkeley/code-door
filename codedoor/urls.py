from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.urls import path

import codedoor.views as views

app_name = 'codedoor'

urlpatterns = [
    url(r'^hello', views.hello, name='hello'),
    url(r'^createprofile', views.createprofile, name='createprofile'),
    path('viewprofile/<int:pk>', views.viewprofile, name='viewprofile'),
    path('editprofile/<int:pk>', views.editprofile, name='editprofile'),
    path('eprofile', views.edit, name='edit'),
]
