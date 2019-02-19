from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.urls import path

import codedoor.views as views

urlpatterns = [
    path('home', views.home, name="home"),
    path('codebank', views.codebank, name="codebank"),
    path('search/<str:database>', views.search, name="search")
]

