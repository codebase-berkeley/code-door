
from django.conf.urls import url
from django.urls import path
from django.conf.urls import url

import codedoor.views as views

urlpatterns = [
    url('addrc/', views.addrc, name='addrc'),
    url('addac/', views.addac, name='addac')
]
