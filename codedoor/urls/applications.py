from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.urls import path

import codedoor.views as views


urlpatterns = [
    path('createapplication', views.create_application_company, {}, name="create_application"),
    path('createapplication/<int:companypk>', views.create_application, name="create_application_filled"),
    path('editapplication/<int:pk>', views.edit_application, name="edit_application"),
    path('viewapplication/<int:pk>', views.view_application, name="view_application"),
    path('listapplications', views.list_all_applications, name="list_all_applications"),
]
