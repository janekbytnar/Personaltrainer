# Generated by Django 4.1.7 on 2023-04-01 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_plans_users_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.plans'),
        ),
    ]