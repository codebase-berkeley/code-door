from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.urls import path

import codedoor.views as views

app_name = 'codedoor'

urlpatterns = [
    path('createquestion', views.create_question, name="create_question"),
    path('editquestion/<int:pk>', views.edit_question, name="edit_question"),
    path('viewquestion/<int:pk>', views.view_question, name="view_question"),
    path('listquestions', views.list_questions, name="list_questions"),
  
    url('createprofile', views.createprofile, name='createprofile'),
    path('viewprofile/<int:pk>', views.viewprofile, name='viewprofile'),
    path('editprofile/<int:pk>', views.editprofile, name='editprofile'),
  
    path('createcompany', views.create_company, name="createcompany"),
    path('viewcompany/<int:pk>', views.view_company, name="viewcompany"),
    path('editcompany/<int:pk>', views.edit_company, name="editcompany"),
]
