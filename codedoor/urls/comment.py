from django.contrib.auth import views as auth_views

from django.conf.urls import url
import codedoor.views as views

urlpatterns = [
    url('comment^addrc/', views.addrc, name='addrc')
]
