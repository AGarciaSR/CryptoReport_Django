from django.shortcuts import render
from .forms import TransactionForm

# Create your views here.
def insert_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request, data=request.POST)
        if form.is_valid():
            '''if user.is_active:
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    messages.info(request, "Credenciales incorrectas, inténtelo de nuevo")
                    return render(request, "users_login.html", {"form": form})
        else:
            messages.info(request, "Credenciales incorrectas, inténtelo de nuevo")
            return render(request, "users_login.html", {"form": form})'''
    else:
        form = TransactionForm()

    return render(request, "transaction_insert.html", {"form": form})