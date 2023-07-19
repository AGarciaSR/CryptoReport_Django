import csv
from .models import Coin, Exchange, Transaction, RawTransaction

def handle_transaction_csv(f):
    stats = {}
    lines_dict = []
    lines = []
    # Número de transacciones encontradas en el CSV
    for line in f:
        # Por cada línea del archivo csv la pasamos a String, dividimos por ";" y eliminamos el carácter de salto de línea
        new_line = str(line).split(";")
        # Eliminamos los 2 primeros caracteres del primer elemento, y los 3 últimos, que son residuales
        new_line[0] = new_line[0][2:]
        new_line[-1] = new_line[-1][:-3]
        lines.append(new_line)
    f.close()
    stats["headers"] = lines[0]
    lines.pop(0)
    stats["number"] = len(lines)
    i = 0
    for line in lines:
        lines_dict.append(dict(zip(stats["headers"],line)))
    stats["transactions"] = lines_dict
    return stats

def create_transaction(data):
    new_transaction = Transaction()
    coin_a = Coin.objects.filter(name=data['pair_a_name']).first()
    coin_b = Coin.objects.filter(name=data['pair_b_name']).first()
    coin_fee = Coin.objects.filter(name=data['coin_fee_name']).first()
    exchange = Exchange.objects.filter(name=data['exchange']).first()
    if coin_a == None:
        coin_a = Coin()
        coin_a.symbol = data['pair_a']
        coin_a.name = data['pair_a_name']
        coin_a.save()
    if coin_b == None:
        coin_b = Coin()
        coin_b.symbol = data['pair_b']
        coin_b.name = data['pair_b_name']
        coin_b.save()
    if coin_fee == None:
        coin_fee = Coin()
        coin_fee.symbol = data['coin_fee']
        coin_fee.name = data['coin_fee_name']
        coin_fee.save()
    if exchange == None:
        exchange = Exchange()
        exchange.name = data['exchange']
        exchange.save()
    new_transaction.user_id = data["id"]
    new_transaction.fecha_hora = data["datetime"]
    new_transaction.mount_a = data['mount_a']
    new_transaction.pair_a = data['pair_a']
    new_transaction.pair_a_name = coin_a
    new_transaction.mount_b = data['mount_b']
    new_transaction.pair_b = data['pair_b']
    new_transaction.pair_b_name = coin_b
    new_transaction.t_type = data['type']
    new_transaction.exchange = exchange
    new_transaction.mount_fee = data['mount_fee']
    new_transaction.coin_fee = data['coin_fee']
    new_transaction.coin_fee_name = coin_fee
    new_transaction.pair_a_coin_value = data['pair_a_coin_value']
    new_transaction.pair_b_coin_value = data['pair_b_coin_value']
    new_transaction.coin_fee_value = data['coin_fee_value']
    new_transaction.order_value = data['order_value']
    new_transaction.fee_value = data['fee_value']
    new_transaction.total_value = data['total_value']
    new_transaction.comment = data['comment']
    new_transaction.save()
    
    if(new_transaction.order_value != 0):
        create_raw_transactions(new_transaction)
    
def create_raw_transactions(transaction):
    # Crear RawTransactions
    if transaction.t_type == 'buy':
        t_type_a = 'buy'
        t_type_b = 'sell'
    else:
        t_type_a = 'sell'
        t_type_b = 'buy'
    
    new_raw_transaction = RawTransaction()
    new_raw_transaction.user_id = transaction.user_id
    new_raw_transaction.fecha_hora = transaction.fecha_hora
    new_raw_transaction.mount_a = transaction.mount_a
    new_raw_transaction.symbol = transaction.pair_a
    new_raw_transaction.coin_name = transaction.pair_a_name
    new_raw_transaction.t_type = t_type_a
    new_raw_transaction.value = transaction.order_value
    new_raw_transaction.coin_value = transaction.pair_a_coin_value
    new_raw_transaction.save()
    
    new_raw_transaction = RawTransaction()
    new_raw_transaction.user_id = transaction.user_id
    new_raw_transaction.fecha_hora = transaction.fecha_hora
    new_raw_transaction.mount_a = transaction.mount_b
    new_raw_transaction.symbol = transaction.pair_b
    new_raw_transaction.coin_name = transaction.pair_b_name
    new_raw_transaction.t_type = t_type_b
    new_raw_transaction.value = transaction.order_value
    new_raw_transaction.coin_value = transaction.pair_b_coin_value
    new_raw_transaction.save()
    
    new_raw_transaction = RawTransaction()
    new_raw_transaction.user_id = transaction.user_id
    new_raw_transaction.fecha_hora = transaction.fecha_hora
    new_raw_transaction.mount_a = transaction.mount_fee
    new_raw_transaction.symbol = transaction.coin_fee
    new_raw_transaction.coin_name = transaction.coin_fee_name
    new_raw_transaction.t_type = 'fee'
    new_raw_transaction.value = transaction.fee_value
    new_raw_transaction.coin_value = transaction.coin_fee_value
    new_raw_transaction.save()