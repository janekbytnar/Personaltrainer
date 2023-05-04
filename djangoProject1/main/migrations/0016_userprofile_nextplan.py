# Generated by Django 4.1.7 on 2023-04-28 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_plans_descriptionlong_alter_plans_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='nextPlan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_plan', to='main.plans'),
        ),
    ]
