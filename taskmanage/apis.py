from .models import Tasks,Checklists
from rest_framework import viewsets, response
from .serializers import IndexSerializer
from collections import namedtuple

Index = namedtuple('Index', ('Tasks', 'Checklists'))
class IndexLists(viewsets.ViewSet):
    def list(self, request):
        index = Index(
            Tasks=Tasks.objects.all(),
            Checklists=Checklists.objects.all(),
        )
        serializer = IndexSerializer(index)
        return response.Response(serializer.data)