# Generated by Django 4.2.2 on 2023-07-04 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extenduser',
            name='coinapi_key',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
