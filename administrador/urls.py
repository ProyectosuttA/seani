from django.urls import path
from .views import *

urlpatterns=[
    path('', administrador, name='administrador'),
    path('listar/', listar, name='listar'),
    path('agregar/', agregar, name='agregar'),
    path('listarp/', listarp, name='listarp'),
    path('archivo/', archivo, name='archivo'),
    path('listaretapa/', listaretapa, name='listaretapa'),
    path('listarmodulo/', listarmodulo, name='listarmodulo'),
    path('agregarpregunta/', agregarpregunta, name='agregarpregunta'),
    path('actualizarusuario/', actualizarusuario, name='actualizarusuario'),
    path('actualizarpregunta/', actualizarpregunta, name='actualizarpregunta'),
    path('eliminarusuario/', eliminarusuario, name='eliminarusuario'),
    path('eliminarpregunta/', eliminarpregunta, name='eliminarpregunta'),
 ]