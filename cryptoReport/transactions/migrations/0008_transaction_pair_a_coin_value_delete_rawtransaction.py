# Generated by Django 4.2.1 on 2023-07-15 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_alter_rawtransaction_pair_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='pair_a_coin_value',
            field=models.FloatField(default=0),
        ),
        migrations.DeleteModel(
            name='RawTransaction',
        ),
    ]
