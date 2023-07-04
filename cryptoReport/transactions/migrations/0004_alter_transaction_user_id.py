# Generated by Django 4.2.2 on 2023-07-04 01:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0003_alter_exchange_url_alter_transaction_coin_fee_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User', to=settings.AUTH_USER_MODEL),
        ),
    ]
