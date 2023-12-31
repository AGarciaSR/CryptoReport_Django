# Generated by Django 4.2.1 on 2023-07-15 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_alter_transaction_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rawtransaction',
            name='user_id',
        ),
        migrations.AddField(
            model_name='rawtransaction',
            name='transaction',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='transactions.transaction'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rawtransaction',
            name='t_type',
            field=models.CharField(choices=[('buy', 'Compra'), ('sell', 'Venta'), ('fee', 'Comision')]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='coin_fee_value',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='fee_value',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='order_value',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='pair_b_coin_value',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='t_type',
            field=models.CharField(choices=[('buy', 'Compra'), ('sell', 'Venta')]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='total_value',
            field=models.FloatField(default=0),
        ),
    ]
