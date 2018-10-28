from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views


from keywordSearchapi import views


app_name = "keywordSearchapi"

urlpatterns = [
    url(r'^home/$', views.index_page),
    url('search', views.search.as_view()),

]