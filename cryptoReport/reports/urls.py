from django.urls import path
from . import views

urlpatterns = [
    path('total_volumes', views.total_volumes, name='total_volumes'),
    path('fees_paid', views.fees_paid, name='fees_paid'),
    path('dca_values', views.dca_values, name='dca_values')
]