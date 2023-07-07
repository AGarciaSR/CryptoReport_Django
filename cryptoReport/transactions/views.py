from django.http import HttpResponse
from django.shortcuts import render
from .forms import TransactionForm, TransactionCSV
from django.contrib.auth.models import User
from .models import Coin, Exchange, Transaction, RawTransaction
from .functions import handle_transaction_csv

# Create your views here.
def insert_transaction(request):
    if request.method == "POST":
        if 'single_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                # Si no hay ya una Coin creada con el nombre pasado por formulario, la creamos en la base de datos
                new_transaction = Transaction()
                coin_a = Coin.objects.filter(name=form.cleaned_data['pair_a_name']).first()
                coin_b = Coin.objects.filter(name=form.cleaned_data['pair_b_name']).first()
                coin_fee = Coin.objects.filter(name=form.cleaned_data['coin_fee_name']).first()
                exchange = Exchange.objects.filter(name=form.cleaned_data['exchange']).first()
                if coin_a == None:
                    coin_a = Coin()
                    coin_a.symbol = form.cleaned_data['pair_a']
                    coin_a.name = form.cleaned_data['pair_a_name']
                    coin_a.save()
                if coin_b == None:
                    coin_b = Coin()
                    coin_b.symbol = form.cleaned_data['pair_b']
                    coin_b.name = form.cleaned_data['pair_b_name']
                    coin_b.save()
                if coin_fee == None:
                    coin_fee = Coin()
                    coin_fee.symbol = form.cleaned_data['coin_fee']
                    coin_fee.name = form.cleaned_data['coin_fee_name']
                    coin_fee.save()
                if exchange == None:
                    exchange = Exchange()
                    exchange.name = form.cleaned_data['exchange']
                    exchange.save()
                print(User.objects.filter(id = request.user.id).first())
                new_transaction.user_id = User.objects.filter(id = request.user.id).first()
                new_transaction.fecha_hora = form.cleaned_data['fecha_hora']
                new_transaction.mount_a = form.cleaned_data['mount_a']
                new_transaction.pair_a = form.cleaned_data['pair_a']
                new_transaction.pair_a_name = coin_a
                new_transaction.mount_b = form.cleaned_data['mount_b']
                new_transaction.pair_b = form.cleaned_data['pair_b']
                new_transaction.pair_b_name = coin_b
                new_transaction.t_type = form.cleaned_data['t_type']
                new_transaction.exchange = exchange
                new_transaction.mount_fee = form.cleaned_data['mount_fee']
                new_transaction.coin_fee = form.cleaned_data['coin_fee']
                new_transaction.coin_fee_name = coin_fee
                new_transaction.pair_b_coin_value = form.cleaned_data['pair_b_coin_value']
                new_transaction.coin_fee_value = form.cleaned_data['coin_fee_value']
                new_transaction.order_value = form.cleaned_data['order_value']
                new_transaction.fee_value = form.cleaned_data['fee_value']
                new_transaction.total_value = form.cleaned_data['total_value']
                new_transaction.comment = form.cleaned_data['comment']
                new_transaction.save()
            '''else:
                messages.info(request, "Credenciales incorrectas, inténtelo de nuevo")
                return render(request, "users_login.html", {"form": form})'''
        elif 'bulk_transaction' in request.POST:
            form = TransactionCSV(request.POST, request.FILES)
            print("Hola1")
            if form.is_valid():
                print("Hola")
                number_t = handle_transaction_csv(request.FILES["archivo"])
                print(number_t)
                return HttpResponse(number_t)
            else:
                print("Hola2")
    else:
        form = TransactionForm()
        form_bulk = TransactionCSV()
        return render(request, "transaction_insert.html", {"form": form, "form_bulk": form_bulk})
    