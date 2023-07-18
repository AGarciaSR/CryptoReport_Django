import requests, datetime
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from .forms import TransactionForm, TransactionCSV
from django.contrib.auth.models import User
from .models import Coin, Exchange, Transaction
from .functions import handle_transaction_csv, create_transaction

# Create your views here.
def insert_transaction(request):
    if request.method == "POST":
        if 'single_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                data = {}
                data["id"] = User.objects.filter(id = request.user.id).first()
                data["pair_a_name"] = form.cleaned_data['pair_a_name']
                data["pair_b_name"] = form.cleaned_data['pair_b_name']
                data["coin_fee_name"] = form.cleaned_data['coin_fee_name']
                data["exchange"] = form.cleaned_data['exchange']
                data["pair_a"] = form.cleaned_data['pair_a']
                data["pair_b"] = form.cleaned_data['pair_b']
                data["coin_fee"] = form.cleaned_data['coin_fee']
                data["datetime"] = form.cleaned_data['fecha_hora']
                data["mount_a"] = form.cleaned_data['mount_a']
                data["mount_b"] = form.cleaned_data['mount_b']
                data["mount_fee"] = form.cleaned_data['mount_fee']
                data["type"] = form.cleaned_data['t_type']
                data['pair_a_coin_value'] = 0
                data['pair_b_coin_value'] = 0
                data['coin_fee_value'] = 0
                data['order_value'] = 0
                data['fee_value'] = 0
                data['total_value'] = 0
                data['comment'] = form.cleaned_data['comment']
                create_transaction(data)
                return(redirect("list_transactions"))
        elif 'bulk_transaction' in request.POST:
            form = TransactionCSV(request.POST, request.FILES)
            if form.is_valid():
                csv_data = handle_transaction_csv(request.FILES["archivo"])
                for data in csv_data["transactions"]:
                    data["id"] = User.objects.filter(id = request.user.id).first()
                    create_transaction(data)
                return render(request, "bulk_transactions.html", {"number": csv_data["number"], "headers": csv_data["headers"], "transactions": csv_data["transactions"]})
            else:
                return HttpResponse("El formulario no es válido")
    else:
        form = TransactionForm()
        form_bulk = TransactionCSV()
        return render(request, "transaction_insert.html", {"form": form, "form_bulk": form_bulk})
    
def list_transactions(request):
    transactions = Transaction.objects.filter(user_id = request.user.id).order_by('-fecha_hora')
    number_transactions = transactions.count()
    paginator = Paginator(transactions, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "n_trans": number_transactions,
        "first_trans": transactions.reverse()[0].fecha_hora,
        "last_trans": transactions[0].fecha_hora
    }
    return render(request, "list_transactions.html", context)

def request_values(request):
    if request.method != "POST":
        empty_transactions = Transaction.objects.only('id').filter(user_id = request.user.id, total_value = 0).order_by('fecha_hora')
        number_transactions = empty_transactions.count()
        context = {
            "n_trans": number_transactions,
            "first_trans": empty_transactions.reverse()[0].fecha_hora,
            "last_trans": empty_transactions[0].fecha_hora
        }
    else:
        empty_transactions = Transaction.objects.only('fecha_hora', 'mount_a', 'pair_a', 'mount_b', 'pair_b', 't_type', 'mount_fee', 'coin_fee').filter(user_id = request.user.id, total_value = 0).order_by('fecha_hora')
        user = request.user
        apikey = user.extenduser.coinapi_key
        t_completed = 0
        headers = {'X-CoinAPI-Key' : apikey}
        limit_reached = False
        for transaction in empty_transactions:
            pair_b = transaction.pair_b
            fecha_hora = transaction.fecha_hora.strftime("%Y-%m-%dT%H:%M:%S")
            fecha_hora_add = transaction.fecha_hora + datetime.timedelta(days=1)
            fecha_hora_add = fecha_hora_add.strftime("%Y-%m-%dT%H:%M:%S")
            url = f'https://rest.coinapi.io/v1/exchangerate/{pair_b}/USD/history?period_id=1SEC&time_start={fecha_hora}&time_end={fecha_hora_add}'
            response = requests.get(url, headers=headers)
            if(response.status_code == 200):
                if response.json() != []:
                    transaction.pair_b_coin_value = response.json()[0]["rate_high"]
                # Si pair_b no está soportada por CoinAPI, hacemos el cálculo en base a pair_a
                else:
                    pair_a = transaction.pair_a
                    url = f'https://rest.coinapi.io/v1/exchangerate/{pair_a}/USD/history?period_id=1SEC&time_start={fecha_hora}&time_end={fecha_hora_add}'
                    response = requests.get(url, headers=headers)
                    transaction.pair_b_coin_value = (response.json()[0]["rate_high"] * transaction.mount_a) / transaction.mount_b
                transaction.order_value = transaction.pair_b_coin_value * transaction.mount_b
                transaction.pair_a_coin_value = transaction.order_value / transaction.mount_a
                # Si la moneda usada para pagar comisión es la misma que pair_b, no se pide el valor
                if transaction.coin_fee == pair_b:
                    transaction.coin_fee_value = transaction.pair_b_coin_value
                else:
                    coin_fee = transaction.coin_fee
                    url = f'https://rest.coinapi.io/v1/exchangerate/{coin_fee}/USD/history?period_id=1SEC&time_start={fecha_hora}&time_end={fecha_hora_add}'
                    response = requests.get(url, headers=headers)
                    transaction.coin_fee_value = response.json()[0]["rate_high"]
                transaction.fee_value = transaction.coin_fee_value * transaction.mount_fee
                # Si ha sido una compra, el valor de la comisión se suma al valor de la operación para obtener el costo total
                if transaction.t_type == "buy":
                    transaction.total_value = transaction.order_value + transaction.fee_value
                # Si ha sido una venta, el valor de la comisión se resta, ya que se obtuvo un rendimiento menor al retorno de la venta
                else:
                    transaction.total_value = transaction.order_value - transaction.fee_value
                transaction.save()
                t_completed += 1
            elif response.status_code == 429:
                limit_reached = True
                break
            
        context = {
            "t_completed": t_completed,
            "limit_reached": limit_reached
        }
    return render(request, "request_values.html", context)