from django.contrib.auth import views as auth_views
from django.conf.urls import url

import codedoor.views as views

app_name='codedoor'

urlpatterns = [
	url(r'^hello', views.hello, name='hello'),
]
