# Generated by Django 4.0.4 on 2022-05-05 00:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('discription', models.TextField(default='未設定', null=True)),
                ('deadline', models.DateTimeField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('participants', models.TextField(default='未設定', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Checklists',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('checked', models.BooleanField()),
                ('parent_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskmanage.tasks')),
            ],
        ),
    ]
