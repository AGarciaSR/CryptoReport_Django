from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import User

class UserLoginForm(forms.BaseForm):
    username = forms.CharField(label="Nombre de usuario", max_length=20, required=True)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email']
        
class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label="Nombre de usuario", max_length=20, required=True)
    first_name = forms.CharField(label="Nombre", max_length=50, required=True)
    last_name = forms.CharField(label="Apellido", max_length=50, required=True)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    email = forms.EmailField()
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email', 'group']