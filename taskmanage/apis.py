from .models import Tasks, Checklists
from rest_framework.viewsets import ModelViewSet
from .serializers import IndexTasksSerializer, ChecklistsSerializer, DetailTaskSerializer

class TasksIndex(ModelViewSet):
    serializer_class = IndexTasksSerializer
    queryset = Tasks.objects.order_by("deadline")

    def get_serializer_class(self, *args, **kwargs):
        if self.action!='list':
            return DetailTaskSerializer
        else:
            return self.serializer_class
            
    def create(self, request, *args, **kwargs):
        response = super(TasksIndex, self).create(request, *args, **kwargs)
        response.data = response.data["uuid"]
        return response

class ChecklistsIndex(ModelViewSet):
    serializer_class = ChecklistsSerializer
    queryset = Checklists.objects.all()

    def get_queryset(self):
        parent = self.request.query_params.get("parent_task")
        if parent:
            return Checklists.objects.filter(parent_task=parent)
        else:
            return self.queryset