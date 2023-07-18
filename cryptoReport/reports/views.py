from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.models import User
from transactions.models import Coin, Exchange, Transaction

# Create your views here.
def total_volumes(request):
    volumes = Transaction.objects.raw("SELECT 1 as id, symbol, pair_a_name_id, SUM(CASE WHEN t_type = 'buy' OR t_type = 'sell' THEN 1 ELSE 0 END) as number, pair_a_name_id, sum(CASE WHEN t_type = 'buy' THEN order_value ELSE 0 END) as volume_buy, SUM(CASE WHEN t_type = 'sell' THEN order_value ELSE 0 END) as volume_sell FROM transactions_transaction JOIN transactions_coin ON transactions_transaction.pair_a_name_id = transactions_coin.name GROUP BY pair_a_name_id, symbol ORDER BY number DESC")
    for volume in volumes:
        volume.total_volume = volume.volume_buy + volume.volume_sell
    context = {
        "volumes": volumes
    }
    return render(request, "total_volumes.html", context)