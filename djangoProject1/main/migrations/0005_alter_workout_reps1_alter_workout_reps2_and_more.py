# Generated by Django 4.1.5 on 2023-03-29 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_workout_description_remove_workout_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='reps1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='reps2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='reps3',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='reps4',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='series',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
