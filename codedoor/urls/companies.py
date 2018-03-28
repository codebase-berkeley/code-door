from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.urls import path

import codedoor.views as views

urlpatterns = [
    path('createcompany', views.create_company, name="createcompany"),
    path('viewcompany/<int:pk>', views.view_company, name="viewcompany"),
    path('editcompany/<int:pk>', views.edit_company, name="editcompany"),
    path('viewcompany/<int:pk>/applications', views.list_applications, name="listcompanies")
]
