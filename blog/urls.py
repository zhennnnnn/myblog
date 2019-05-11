from django.urls import path,re_path
from django.contrib import admin
from . import views

urlpatterns = [
    path('list', views.post_list, name='post_list'),
    path('create', views.post_create, name='post_create'),
    path('index/',views.index),
    path('login/',views.login),
    path('logout/',views.logout),
    path('register/',views.register),
    path('crawler/',views.crawler),
    re_path('detail/(\d+)/$',views.detail)
]

#from gameapp import views