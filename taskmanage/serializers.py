from rest_framework import serializers
from .models import Tasks,Checklists

class IndexTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['uuid', 'title', 'deadline']

class ChecklistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklists
        fields = ['uuid', 'content', 'checked', 'parent_task']