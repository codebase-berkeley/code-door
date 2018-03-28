from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.urls import path

import codedoor.views as views

urlpatterns = [
    path('createreview', views.create_review, name="createreview"),
    path('viewreview/<int:pk>', views.view_review, name="viewreview"),
    path('editreview/<int:pk>', views.edit_review, name="editreview"),
]
