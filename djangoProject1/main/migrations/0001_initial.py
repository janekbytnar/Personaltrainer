# Generated by Django 4.1.5 on 2023-03-29 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('video', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Plans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('priceMonthly', models.IntegerField()),
                ('priceYearly', models.IntegerField()),
                ('description', models.TextField()),
                ('sex', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('day', models.IntegerField()),
                ('series', models.IntegerField()),
                ('reps', models.IntegerField()),
                ('exercises', models.ManyToManyField(to='main.exercise')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.plans')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.plans')),
            ],
        ),
    ]
