from django.urls import path
from .views import *

urlpatterns=[
    path('', inicio, name='inicio'),
    path('ingresar', ingresar, name='ingresar'),
    path('registrar', registrar, name='registrar'),
    path('salir', salir, name='salir'),
 ]