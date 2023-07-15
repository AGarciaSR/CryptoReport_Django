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
    comment = forms.CharField(max_length=200, required=False)
        
    class Meta:
        model = Transaction
        exclude = ['user_id', 'pair_a_name', 'pair_b_name', 'coin_fee_name', 'exchange', 'pair_b_coin_value', 'coin_fee_value', 'order_value', 'fee_value', 'total_value']
        fields = ['fecha_hora','mount_a','pair_a', 'mount_b','pair_b', 't_type','mount_fee','coin_fee', 'comment']
        
class TransactionCSV(forms.Form):
    archivo = forms.FileField()    
    