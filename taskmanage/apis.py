from .models import Tasks,Checklists
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .serializers import IndexTasksSerializer, ChecklistsSerializer, DetailTaskSerializer

class TasksIndex(ModelViewSet):
    queryset = Tasks.objects.order_by("deadline")

    @action(detail=True, methods=['get'])
    def get_serializer_class(self, pk=None, *args, **kwargs):
        if self.kwargs.get("pk"):
            return DetailTaskSerializer
        else:
            return IndexTasksSerializer

class ChecklistsIndex(ModelViewSet):
    serializer_class = ChecklistsSerializer
    queryset = Checklists.objects.all()