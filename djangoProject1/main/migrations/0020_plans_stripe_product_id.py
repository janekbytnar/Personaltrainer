# Generated by Django 4.1.7 on 2023-04-30 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='plans',
            name='stripe_product_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
