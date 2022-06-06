from asyncio import tasks
from rest_framework import serializers
from .models import Tasks,Checklists

class IndexTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['uuid', 'title', 'deadline']

class DetailTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['uuid', 'title', 'discription', 'deadline', 'created_at', 'updated_at', 'participants']

class ChecklistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklists
        fields = ['uuid', 'content', 'checked', 'parent_task']