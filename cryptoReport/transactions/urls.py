from django.urls import path
from . import views

urlpatterns = [
    path('insert_transaction', views.insert_transaction, name='insert_transaction')
]