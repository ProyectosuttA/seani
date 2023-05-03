from django.urls import path
from .views import *

urlpatterns=[
    path('', examen, name='examen'),
    path('<int:id_mod>', modulo, name='modulo'),
    path('<int:id_mod>/pregunta/<int:id_ques>', question, name="question"),
    path('modulo/<int:id_mod>/save', save_modulo, name="save_modulo")
 ]