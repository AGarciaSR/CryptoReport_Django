from django.urls import path
from . import views

urlpatterns = [
    path('', views.users_index, name='users_index'),
    path('login', views.users_login, name='users_login'),
    path('logout', views.users_logout, name='users_logout'),
    path('register', views.users_register, name='users_register'),
    path('my_profile', views.users_profile, name='users_profile')
]