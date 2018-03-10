from django.contrib.auth import views as auth_views
from django.conf.urls import url

import codedoor.views as views

app_name='codedoor'

urlpatterns = [
	url(r'^hello', views.hello, name='hello'),
	url(r'^createprofile', views.createprofile, name = 'createprofile'),
	url(r'^viewprofile', views.viewprofile, name = 'viewprofile'),
	url(r'^editprofile', views.editprofile, name = 'editprofile'),
	url(r'^profilecreated', views.profilecreated, name = 'profilecreated')
]
