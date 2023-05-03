from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate 
import csv
from administrador.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse

# Create your views here.
def inicio(request):
    """usuarios=User.objects.all()
    for usuario in usuarios:
        print(usuario.is_superuser)"""

    if request.user.is_authenticated:
        logout(request)
        return render(request, 'bienvenida/index.html')
    else:
        return render(request, 'bienvenida/index.html')

def registrar(request):
    if request.method=='GET':
        return render(request,'bienvenida/registrar.html',{'form':UserCreationForm})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password2'])
                user.firstname=request.POST['nombres'] 
                user.lastname=request.POST['apellidos'] 
                user.email=request.POST['username'] 
                user.save()
                login(request, user)
                print(user.is_superuser)
                return render(request,'bienvenida/registrar.html',{'form':UserCreationForm, 'error':'El usuario fue creado correctamente'})
            except:
                return render(request,'bienvenida/registrar.html',{'form':UserCreationForm,'error':'El usuario ya existe'})
        else:     
            return render(request,'bienvenida/registrar.html',{'form':UserCreationForm, 'error':'Las contraseñas no son las mismas'})

     
def ingresar(request):
    if request.method=='GET':
        return render(request,'bienvenida/ingresar.html')
    else:
        user=authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'bienvenida/ingresar.html',{'error':'Revisa el usuario y la contraseña'})
        else:
            login(request, user)
            if user.is_superuser == True:
                return redirect('administrador')
            else:
                return redirect('examen')


def salir(request):
    logout(request)
    return redirect('inicio')





