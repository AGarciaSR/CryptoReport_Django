from django import forms
from django.contrib.auth.forms import User
from .models import Transaction

class TransactionForm(forms.ModelForm):
    fecha_hora = forms.DateTimeField()
    mount_a = forms.FloatField()
    pair_a = forms.CharField(max_length=10)
    pair_a_name = forms.CharField(max_length=40)
    mount_b = forms.FloatField()
    pair_b = forms.CharField(max_length=10)
    pair_b_name = forms.CharField(max_length=40)
    t_type = forms.ChoiceField
    exchange = forms.CharField(max_length=40)
    mount_fee = forms.FloatField()
    coin_fee = forms.CharField(max_length=10)
    coin_fee_name = forms.CharField(max_length=40)
    pair_b_coin_value = forms.FloatField()
    coin_fee_value = forms.FloatField()
    order_value = forms.FloatField()
    fee_value = forms.FloatField()
    total_value = forms.FloatField()
    comment = forms.CharField(max_length=200)
    
    def __init__(self):
        super(TransactionForm, self).__init__()
        
    class Meta:
        model = Transaction
        fields = ['fecha_hora','mount_a','pair_a','pair_a_name','mount_b','pair_b','pair_b_name','t_type','exchange','mount_fee','coin_fee','coin_fee_name','pair_b_coin_value','coin_fee_value','order_value','fee_value','total_value','comment']