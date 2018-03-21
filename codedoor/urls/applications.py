from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.urls import path

import codedoor.views as views

urlpatterns = [
	path('createquestion', views.create_application, name="create_application"),
    path('editquestion/<int:pk>', views.edit_application, name="edit_application"),
    path('viewquestion/<int:pk>', views.view_application, name="view_application"),
]

