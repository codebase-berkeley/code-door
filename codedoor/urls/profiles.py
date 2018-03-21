from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.urls import path

import codedoor.views as views

urlpatterns = [
    path('createprofile/', views.createprofile, name='createprofile'),
    path('viewprofile/<int:pk>', views.viewprofile, name='viewprofile'),
    path('editprofile/<int:pk>', views.editprofile, name='editprofile'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
]
