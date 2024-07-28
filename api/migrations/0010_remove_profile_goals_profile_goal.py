# Generated by Django 5.0.6 on 2024-07-07 01:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_goal_delete_goalform_alter_profile_goals'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='goals',
        ),
        migrations.AddField(
            model_name='profile',
            name='goal',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.goal'),
        ),
    ]