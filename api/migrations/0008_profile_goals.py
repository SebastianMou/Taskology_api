# Generated by Django 5.0.6 on 2024-07-06 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_goalform'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='goals',
            field=models.ManyToManyField(blank=True, null=True, to='api.goalform'),
        ),
    ]