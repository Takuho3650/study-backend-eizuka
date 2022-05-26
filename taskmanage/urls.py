from email.mime import base
from . import views
from django.contrib import admin
from django.urls import path, include
from . import apis
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'tasks', apis.IndexLists, basename='Tasks')

urlpatterns = [
    path('', include(router.urls)),
]