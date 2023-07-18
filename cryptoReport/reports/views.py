from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.models import User
from transactions.models import Coin, Exchange, Transaction

# Create your views here.
def total_volumes(request):
    volumes = Transaction.objects.raw("SELECT 1 as id, symbol, pair_a_name_id, SUM(CASE WHEN t_type = 'buy' OR t_type = 'sell' THEN 1 ELSE 0 END) as number, pair_a_name_id, sum(CASE WHEN t_type = 'buy' THEN order_value ELSE 0 END) as volume_buy, SUM(CASE WHEN t_type = 'sell' THEN order_value ELSE 0 END) as volume_sell FROM transactions_transaction JOIN transactions_coin ON transactions_transaction.pair_a_name_id = transactions_coin.name WHERE transactions_transaction.user_id_id = "+str(request.user.id)+" GROUP BY pair_a_name_id, symbol ORDER BY symbol ASC")
    num_coins = Transaction.objects.only("pair_a_name").distinct("pair_a_name")
    for volume in volumes:
        volume.total_volume = volume.volume_sell - volume.volume_buy
    context = {
        "volumes": volumes,
        "n_coins": len(num_coins)
    }
    return render(request, "total_volumes.html", context)

def fees_paid(request):
    fees = Transaction.objects.raw("SELECT 1 as id, coin_fee_name_id, SUM(t.mount_fee) as mount, SUM(t.fee_value) as value WHERE transactions_transaction.user_id_id = "+str(request.user.id)+" AND order_value > 0 GROUP BY coin_fee_name_id ORDER BY value")
    context = {
        "fees": fees
    }
    return render(request, "fees_paid.html", context)