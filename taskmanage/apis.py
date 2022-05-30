from .models import Tasks,Checklists
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import IndexTasksSerializer, ChecklistsSerializer

class TasksIndex(ModelViewSet):
    serializer_class = IndexTasksSerializer
    queryset = Tasks.objects.order_by("deadline")

class ChecklistsIndex(ModelViewSet):
    serializer_class = ChecklistsSerializer
    queryset = Checklists.objects.all()