from rest_framework import serializers
from .models import Tasks,Checklists

class IndexTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['uuid', 'title', 'deadline']

class DetailTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'

class ChecklistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklists
        fields = '__all__'