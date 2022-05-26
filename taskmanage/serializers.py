from rest_framework import serializers
from .models import Tasks,Checklists

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('uuid','title','discription')

class ChecklistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklists
        fields = ('uuid', 'checked','parent_task')

class IndexSerializer(serializers.Serializer):
    Tasks = TasksSerializer(many=True)
    Checklists = ChecklistsSerializer(many=True)