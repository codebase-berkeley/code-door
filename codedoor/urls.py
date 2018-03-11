from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.urls import path

import codedoor.views as views

app_name='codedoor'

urlpatterns = [
	path('createcompany', views.create_company, name="createcompany"),
	path('viewcompany/<int:pk>', views.view_company, name="viewcompany"),
	path('editcompany/<int:pk>', views.edit_company, name="editcompany"),
]
