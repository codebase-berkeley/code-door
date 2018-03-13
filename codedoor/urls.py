from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.urls import path

import codedoor.views as views

app_name='codedoor'

urlpatterns = [
	url(r'^hello', views.hello, name='hello'),
	path('createquestion', views.createQPage, name="createQuestion"),
	path('creatingquestion', views.createQ, name="creatingQuestion"),
	path('editquestion/<int:pk>', views.editQPage, name="editQueston"),
    path('editingquestion', views.editQ, name="editingQuestion"),
	# path('eidtQuestion', views.editQ, name="editQuestion"),
	# path('viewQuestion', views.viewQ, name="viewQuestion"),
	# path('listQuestion', views.listQ, name="listQuestion"),
]
