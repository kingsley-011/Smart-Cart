from django.urls import path, re_path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('register', user_register, name='user_register'),
    path('refer', refer_and_earn, name='refer_and_earn'),
    path('cart1', cart1_page, name='cart1'),
    path('cart2', cart2_page, name='cart2'),
    path('payment', payment, name='payment'),
    path('error', error_handle, name='error'),
    path('success', success_handle, name='success'),
    path('login', user_login, name='login'),
    re_path(r'^(?P<id>\d+)/[a-zA-Z0-9]+/$', refferral_system, name='refferal_system')
    
]
