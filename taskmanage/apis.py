from .models import Tasks,Checklists
from rest_framework.viewsets import ModelViewSet
from .serializers import IndexTasksSerializer, ChecklistsSerializer, DetailTaskSerializer

class TasksIndex(ModelViewSet):
    queryset = Tasks.objects.order_by("deadline")

    def get_serializer_class(self, pk=None, *args, **kwargs):
        if self.action!='list':
            return DetailTaskSerializer
        else:
            return IndexTasksSerializer
            
    def create(self, request, *args, **kwargs):
        response = super(TasksIndex, self).create(request, *args, **kwargs)
        response.data = {"uid": response.data["uuid"]}
        return response

class ChecklistsIndex(ModelViewSet):
    serializer_class = ChecklistsSerializer
    queryset = Checklists.objects.all()