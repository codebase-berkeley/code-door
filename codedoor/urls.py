from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.urls import path

import codedoor.views as views

app_name='codedoor'

urlpatterns = [
    url(r'^hello', views.hello, name='hello'),
    
    path('createquestion', views.createQPage, name="createQuestion"),
    path('creatingquestion', views.createQ, name="creatingQuestion"),
    path('editingquestion/<int:pk>', views.editQ, name="editingQuestion"),
    path('editquestion/<int:pk>', views.editQPage, name="editQueston"),
    path('viewquestion/<int:pk>', views.viewQ, name="viewQuestion"),
    path('listquestions', views.listQ, name="listQuestion"),
]
