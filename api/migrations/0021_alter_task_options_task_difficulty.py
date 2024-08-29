# Generated by Django 5.0.6 on 2024-08-28 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_taskanalysis'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('difficulty', 'position', 'created_at'), 'verbose_name_plural': 'tasks'},
        ),
        migrations.AddField(
            model_name='task',
            name='difficulty',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
