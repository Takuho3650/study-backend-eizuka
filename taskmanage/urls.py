from email.mime import base
from . import views
from django.urls import path, include
from . import apis
from rest_framework import routers

router = routers.DefaultRouter()
router.register('task', apis.TasksIndex)
router.register('checklist', apis.ChecklistsIndex)

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.redirecthome.as_view(), name="redirect"),
    path("home/", views.home.as_view(), name="home"),
    path("maketask/", views.maketask.as_view(), name="maketask"),
    path("detail/<uuid:pk>/", views.detail.as_view(), name="detail"),
    path("edittask/<uuid:pk>/", views.edit.as_view(), name="edittask"),
    path("deletetask/<uuid:pk>/", views.deletetask, name="delete")
]