# Generated by Django 5.0.6 on 2024-07-08 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_profile_goals_profile_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='due_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='due date'),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='due created'),
        ),
    ]