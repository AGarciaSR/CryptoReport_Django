import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Coin(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=30, primary_key=True)
    logo = models.CharField(max_length=300, null=True)
    
class Exchange(models.Model):
    name = models.CharField(max_length=40, primary_key=True)
    url = models.CharField(max_length=400, null=True)
    logo = models.CharField(max_length=400, null=True)
    
class Transaction(models.Model):
    class TransactionType(models.Choices):
        COMPRA = "buy"
        VENTA = "sell"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, related_name="User", on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(null=False)
    mount_a = models.FloatField(null=False)
    pair_a = models.CharField(max_length=10, null=False)
    pair_a_name = models.ForeignKey(Coin, related_name="Pair_A_name", on_delete=models.DO_NOTHING)
    mount_b = models.FloatField(null=False)
    pair_b = models.CharField(max_length=10, null=False)
    pair_b_name = models.ForeignKey(Coin, related_name="Pair_B_name", on_delete=models.DO_NOTHING)
    t_type = models.CharField(choices=TransactionType.choices, null=False)
    exchange = models.ForeignKey(Exchange, related_name="Exchange_name", on_delete=models.DO_NOTHING)
    mount_fee = models.FloatField(null=False)
    coin_fee = models.CharField(max_length=10, null=False)
    coin_fee_name = models.ForeignKey(Coin, related_name="Coin_Fee_name", on_delete=models.DO_NOTHING)
    pair_b_coin_value = models.FloatField(null=True)
    coin_fee_value = models.FloatField(null=True)
    order_value = models.FloatField(null=True)
    fee_value = models.FloatField(null=True)
    total_value = models.FloatField(null=True)
    comment = models.CharField(max_length=200)
    
class RawTransaction(models.Model):
    class TransactionType(models.Choices):
        Compra = "buy"
        Venta = "sell"
        Comision = "fee"
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    mount = models.FloatField(null=False)
    pair = models.CharField(max_length=10, null=False)
    pair_name = models.ForeignKey(Coin, on_delete=models.DO_NOTHING)
    t_type = models.CharField(choices=TransactionType.choices, null=False)
    value = models.FloatField(null=True)
    price_per_coin = models.FloatField(null=True)
    