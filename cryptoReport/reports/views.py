from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.models import User
from transactions.models import Coin, Exchange, Transaction, RawTransaction

def total_volumes(request):
    # Dividir la RawQuery en varias líneas para una mejor comprensión
    query = "SELECT 1 as id, symbol, pair_a_name_id, SUM(CASE WHEN t_type = 'buy' THEN mount_a ELSE 0 END) as mount_buy,"
    query += "SUM(CASE WHEN t_type = 'buy' THEN 1 ELSE 0 END) as num_buy,"
    query += "SUM(CASE WHEN t_type = 'sell' THEN 1 ELSE 0 END) as num_sell,"
    query += "SUM(CASE WHEN t_type = 'sell' THEN mount_a ELSE 0 END) as mount_sell,"
    query += "SUM(CASE WHEN t_type = 'buy' THEN order_value ELSE 0 END) as volume_buy,"
    query += "SUM(CASE WHEN t_type = 'sell' THEN order_value ELSE 0 END) as volume_sell,"
    query += "(SUM(CASE WHEN t_type = 'sell' THEN order_value ELSE 0 END) - sum(CASE WHEN t_type = 'buy' THEN order_value ELSE 0 END)) as gainloss "
    query += "FROM transactions_transaction JOIN transactions_coin ON transactions_transaction.pair_a_name_id = transactions_coin.name "
    query += "WHERE transactions_transaction.user_id_id = "+str(request.user.id)
    query += " GROUP BY pair_a_name_id, symbol ORDER BY gainloss DESC"
    volumes = Transaction.objects.raw(query)
    num_coins = Transaction.objects.only("pair_a_name").distinct("pair_a_name")
    max_volume = Transaction.objects.raw("SELECT * FROM transactions_transaction WHERE order_value = (SELECT MAX(order_value) FROM transactions_transaction WHERE transactions_transaction.user_id_id = "+str(request.user.id)+")")
    for volume in volumes:
        volume.total_volume = volume.volume_sell - volume.volume_buy
    context = {
        "volumes": volumes,
        "n_coins": len(num_coins),
        "max_volume": max_volume
    }
    return render(request, "total_volumes.html", context)

def fees_paid(request):
    query = "SELECT 1 as id, coin_fee, coin_fee_name_id, SUM(mount_fee) as mount,"
    query += "SUM(fee_value) as value"
    query += " FROM transactions_transaction JOIN transactions_coin ON transactions_transaction.pair_a_name_id = transactions_coin.name"
    query += " WHERE transactions_transaction.user_id_id = "+str(request.user.id)+" AND order_value > 0"
    query += " GROUP BY coin_fee_name_id, coin_fee ORDER BY value DESC"
    fees = Transaction.objects.raw(query)
    context = {
        "fees": fees
    }
    return render(request, "fees_paid.html", context)

def dca_values(request):
    query = "SELECT 1 as id, transactions_rawtransaction.symbol as symb, coin_name_id,"
    query += "AVG(CASE WHEN t_type = 'buy' THEN coin_value END) as dca_buy,"
    query += "AVG(CASE WHEN t_type = 'sell' OR t_type = 'fee' THEN coin_value END) as dca_sell "
    query += "FROM transactions_rawtransaction JOIN transactions_coin ON transactions_rawtransaction.coin_name_id = transactions_coin.name "
    query += "WHERE transactions_rawtransaction.user_id_id = "+str(request.user.id)
    query += " GROUP BY coin_name_id, symb ORDER BY symb ASC"
    dca = RawTransaction.objects.raw(query)
    context = {
        "dcas": dca
    }
    return render(request, "dca.html", context)