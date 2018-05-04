from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.urls import path

import codedoor.views as views

urlpatterns = [
    path('createreview', views.create_review, name="createreview"),
    path('createreviewwc/<int:pk>', views.create_review_wc, name="createreviewwc"),
    path('viewreview/<int:pk>', views.view_review, name="viewreview"),
    path('editreview/<int:pk>', views.edit_review, name="editreview"),
    path('createdreview', views.created_review, name="created_review"),
    path('viewcompanyreviews', views.view_company_reviews, name="view_company_reviews"),
]
