from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("", views.redirecthome.as_view(), name="redirect"),
    path("home/", views.home.as_view(), name="home"),
    path("maketask/", views.maketask.as_view(), name="maketask"),
    path("detail/<uuid:pk>/", views.detail.as_view(), name="detail"),
    path("edittask/<uuid:pk>/", views.edit.as_view(), name="edittask"),
    path("deletetask/<uuid:task_pk>/", views.deletetask, name="delete")
]