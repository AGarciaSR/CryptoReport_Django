from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from .forms import UserRegisterForm
import time

# Create your views here.
def users_index(request):
    template = loader.get_template('users_index.html')
    return HttpResponse(template.render())

def users_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user.is_active:
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    messages.info(request, "Credenciales incorrectas, inténtelo de nuevo")
                    return render(request, "users_login.html", {"form": form})
        else:
            messages.info(request, "Credenciales incorrectas, inténtelo de nuevo")
            return render(request, "users_login.html", {"form": form})
    else:
        form = AuthenticationForm()

    return render(request, "users_login.html", {"form": form})

def users_logout(request):
    logout(request)
    return redirect('index')

def users_register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = User()
            new_user.username = form.cleaned_data['username']
            new_user.password = make_password(form.cleaned_data['password'])
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.groups.add(Group.objects.get(name=form.cleaned_data['group']))
            return HttpResponse("Gracias, el usuario ha sido agregado")
    else:
        form = UserRegisterForm()

    return render(request, "users_register.html", {"form": form})

# Vista para editar los datos del perfil
def users_profile(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = User()
            new_user.username = form.cleaned_data['username']
            new_user.password = make_password(form.cleaned_data['password'])
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.groups.add(Group.objects.get(name=form.cleaned_data['group']))
            return HttpResponse("Gracias, el usuario ha sido agregado")
    else:
        form = UserRegisterForm()