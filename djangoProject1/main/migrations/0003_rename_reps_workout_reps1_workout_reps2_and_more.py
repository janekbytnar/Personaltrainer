# Generated by Django 4.1.5 on 2023-03-29 14:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_exercise_partofbody'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workout',
            old_name='reps',
            new_name='reps1',
        ),
        migrations.AddField(
            model_name='workout',
            name='reps2',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workout',
            name='reps3',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workout',
            name='reps4',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
