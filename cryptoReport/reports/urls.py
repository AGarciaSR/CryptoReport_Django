from django.urls import path
from . import views

urlpatterns = [
    path('total_volumes', views.total_volumes, name='total_volumes')
]