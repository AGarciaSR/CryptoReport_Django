from django.urls import path
from . import views

urlpatterns = [
    path('insert_transaction', views.insert_transaction, name='insert_transaction'),
    path('list_transactions', views.list_transactions, name='list_transactions'),
    path('request_values', views.request_values, name='request_values')
]