# Generated by Django 5.0.6 on 2024-07-07 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_profile_goals'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_working_on', models.TextField(blank=True)),
                ('progress_towards_goals', models.TextField(blank=True)),
                ('challenges', models.TextField(blank=True)),
                ('one_year_goal', models.TextField(blank=True)),
                ('five_year_goal', models.TextField(blank=True)),
                ('achievements_feel_successful', models.TextField(blank=True)),
                ('motivation', models.TextField(blank=True)),
                ('values_principles', models.TextField(blank=True)),
                ('resources_support', models.TextField(blank=True)),
                ('skills_needed', models.TextField(blank=True)),
            ],
        ),
        migrations.DeleteModel(
            name='GoalForm',
        ),
        migrations.AlterField(
            model_name='profile',
            name='goals',
            field=models.ManyToManyField(blank=True, null=True, to='api.goal'),
        ),
    ]
