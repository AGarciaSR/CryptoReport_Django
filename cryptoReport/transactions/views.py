from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from .forms import TransactionForm, TransactionCSV
from django.contrib.auth.models import User
from .models import Coin, Exchange, Transaction, RawTransaction
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
                data['pair_b_coin_value'] = form.cleaned_data['pair_b_coin_value']
                data['coin_fee_value'] = form.cleaned_data['coin_fee_value']
                data['order_value'] = form.cleaned_data['order_value']
                data['fee_value'] = form.cleaned_data['fee_value']
                data['total_value'] = form.cleaned_data['total_value']
                data['comment'] = form.cleaned_data['comment']
                create_transaction(data)
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