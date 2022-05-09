import uuid
from django.db import models

class Tasks(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    discription = models.TextField(null=True, default='未設定')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    participants = models.TextField(null=True, default='未設定')

    def __str__(self):
        return self.title

class Checklists(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    checked = models.BooleanField()
    parent_task = models.ForeignKey(Tasks, on_delete=models.CASCADE)

# Create your models here.
