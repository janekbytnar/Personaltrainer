# Generated by Django 4.1.5 on 2023-03-29 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_reps_workout_reps1_workout_reps2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workout',
            name='description',
        ),
        migrations.RemoveField(
            model_name='workout',
            name='name',
        ),
    ]
