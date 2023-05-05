from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
import csv
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
import matplotlib.pyplot as plt
from django.contrib.sessions.models import Session
from django.utils import timezone
import mpld3
import numpy as np
import pandas as pd


# Create your views here.
def administrador(request):
    if request.user.is_authenticated:
        user=request.user.is_superuser
        if user == True:
             # Obtener todas las sesiones activas
            active_sessions = Session.objects.filter(expire_date__gte=timezone.now())

             # Contar el número total de sesiones activas
            num_active_sessions = active_sessions.count()

            # Generar el gráfico de pastel
            labels = ['Sesiones activas', 'Sesiones inactivas']
            sizes = [num_active_sessions, Session.objects.count() - num_active_sessions]
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            ax.set_title('Sesiones activas')

            # Convertir el gráfico en código HTML utilizando mpld3
            chart_html = mpld3.fig_to_html(fig)
            # Convertir la gráfica en un objeto HTML
            chart_html = mpld3.fig_to_html(fig)

            #Segunda grafica
            preguntas = ExamenesExam.objects.all()
            suma1=0
            suma2=0
            suma3=0
            suma4=0
            usuarios=0
            for pregunta in preguntas:
                suma1=pregunta.result_mod_1+suma1
                suma2=pregunta.result_mod_2+suma2
                suma3=pregunta.result_mod_3+suma3
                suma4=pregunta.result_mod_4+suma4
                usuarios=usuarios+1
            promedio1=suma1/usuarios
            promedio2=suma2/usuarios
            promedio3=suma3/usuarios
            promedio4=suma4/usuarios
           
            y_data = np.array([promedio1,promedio2,promedio3,promedio4])
            x_names = ['U', 'D', 'L', 'M']
            x_data = np.arange(len(x_names))
            # Crear la gráfica
            fig, ax = plt.subplots()
            ax.scatter(x_data, y_data)
            ax.set_xlabel('Modulos')
            ax.set_ylabel('Resultados')
            ax.set_title('Promedios de los alumnos')
            ax.set_xticklabels(x_names)
            plt.xticks(x_data, x_names)
            fig.tight_layout()
            # Convertir la gráfica en un objeto HTML
            barras = mpld3.fig_to_html(fig) 
            return render(request, 'admin/admin.html',{'grafica':chart_html, 'barras':barras})
        else:
            return redirect('examen')
    else:
        return redirect('inicio')

def listar(request):
    if request.user.is_authenticated:
        user=request.user.is_superuser
        if user == True:
            usuarios=User.objects.all().order_by('id')
            carrera=[]
            mod1=[]
            mod2=[]
            mod3=[]
            mod4=[]
            for usuario in usuarios:
                var=usuario.id
                carrera.append(ExamenesExam.objects.filter(user_id=var).values('career').first())
                mod1.append(ExamenesExam.objects.filter(user_id=var).values('result_mod_1').first())      
                mod2.append(ExamenesExam.objects.filter(user_id=var).values('result_mod_2').first())      
                mod3.append(ExamenesExam.objects.filter(user_id=var).values('result_mod_3').first())      
                mod4.append(ExamenesExam.objects.filter(user_id=var).values('result_mod_4').first())      
            datos = list(zip(usuarios, carrera, mod1,mod2,mod3,mod4))            
            return render(request, 'admin/listar.html',{'usuarios':datos})
        else:
            return redirect('examen')
    else:
        return redirect('inicio')

def agregar(request):
    if request.user.is_authenticated:
        user=request.user.is_superuser
        if user == True:
            if request.method=='GET':
                return render(request, 'admin/agregar.html')
            else:
                try:
                    usuario=User.objects.create_user(email=request.POST['email'].strip(),username=request.POST['email'].strip(), password=request.POST['password'].strip())
                    usuario.first_name=request.POST['nombres']
                    usuario.last_name=request.POST['apellidos']
                    usuario.save()
                    etapa=ExamenesStage.objects.get(no_stage=request.POST['etapa'])
                    exam=usuario.examenesexam_set.create(stage=etapa, career=request.POST['carrera'])
                    preguntas = PreguntasQuestion.objects.all()
                    for pregunta in preguntas:
                        exam.examenesbreakdown_set.create(question=pregunta, correct=pregunta.correct)
                    error="LOS USUARIOS FUERON CREADOS "
                    return render(request, 'admin/agregar.html',{'error':error})                   
                except:
                    error:'El usuario no fue possible crear'
                    return render(request, 'admin/agregar.html',{'error':error})

                return render(request, 'admin/agregar.html')
                
        else:
            return redirect('examen')
    else:
        return redirect('inicio')

def listarp(request):
    if request.user.is_authenticated:
        user=request.user.is_superuser
        if user == True:
            preguntas=PreguntasQuestion.objects.all().order_by('id')                       
            return render(request, 'admin/listar_p.html',{'preguntas':preguntas})
        else:
            return redirect('examen')
    else:
        return redirect('inicio')

def agregarpregunta(request):
    if request.user.is_authenticated:
        user=request.user.is_superuser
        if user == True:
            if request.method=='GET':
                return render(request,'admin/agregar_pregunta.html')
            else:
                return render(request,'admin/agregar_agregar_pregunta.html')                
        else:
            return redirect('examen')
    else:
        return redirect('inicio')

def listaretapa(request):
    if request.user.is_authenticated:
        user=request.user.is_superuser
        if user == True:
            etapas=ExamenesStage.objects.all().order_by('id')                       
            return render(request, 'admin/listar_etapa.html',{'etapas':etapas})
        else:
            return redirect('examen')
    else:
        return redirect('inicio')

def listarmodulo(request):
    if request.user.is_authenticated:
        user=request.user.is_superuser
        if user == True:
            modulos=PreguntasModule.objects.all().order_by('id')                       
            return render(request, 'admin/listar_modulo.html',{'modulos':modulos})
        else:
            return redirect('examen')
    else:
        return redirect('inicio')

def archivo(request):
    if request.user.is_authenticated:
        user=request.user.is_superuser
        if user == True:
            if request.method == 'GET':
                return render(request,'admin/archivo.html') 
            else:
                if request.method == 'POST':
                    csv_file = request.FILES['csv_file']
                    datos = pd.read_csv(csv_file)
                    for dato in datos.to_dict('records'):
                        try:
                            user=User.objects.create_user(email=dato['email'].strip(),username=dato['email'].strip(), password=dato['password'].strip())
                            user.first_name=dato['nombre'].strip()
                            user.last_name=dato['apellidos'].strip()
                            user.save()
                            etapa=ExamenesStage.objects.get(no_stage=dato['etapa'])
                            exam=user.examenesexam_set.create(stage=etapa, career=dato['carrera'])
                            preguntas = PreguntasQuestion.objects.all()
                            for pregunta in preguntas:
                                exam.examenesbreakdown_set.create(question=pregunta, correct=pregunta.correct)
                            error="LOS USUARIOS FUERON CREADOS "
                        except:
                            error="REVISA LA ESTRUCTURA POR FAVOR" 
                    return render(request, 'admin/archivo.html',{'error':error} )
                    
            return render(request, 'admin/archivo.html' )
        else:
            return redirect('examen')
    else:
        return redirect('inicio')

def actualizarusuario(request):
    if request.user.is_authenticated:
        user=request.user.is_superuser
        if user == True:
            if request.method=='GET':
                return render(request, 'admin/actualizar_usuario.html')
            else:       
                try:
                    usuario=User.objects.get(username=request.POST['val'])
                    usuario.username=request.POST['username']
                    usuario.email=request.POST['email']
                    usuario.first_name=request.POST['nombres']
                    usuario.last_name=request.POST['apellidos']
                    pas=make_password(request.POST['password'])
                    usuario.password=pas
                    usuario.save()
                    error="EL USUARIO FUE ACTUALIZADO"  
                    return render(request,'admin/actualizar_usuario.html',{'error':error})

                except:
                    error='ESTE USUARIO NO EXISTE'
                    return render(request,'admin/actualizar_usuario.html',{'error':error})            
                return render(request,'admin/actualizar_usuario.html',{'error':error})                
        else:
            return redirect('examen')
    else:
        return redirect('inicio')

def actualizarpregunta(request):
    if request.user.is_authenticated:
        user=request.user.is_superuser
        if user == True:
            if request.method=='GET':
                return render(request, 'admin/actualizar_pregunta.html')
            else:       
                try:
                    pregunta=PreguntasQuestion.objects.get(id=request.POST['val'])
                    if request.POST['pregunta']!='' and request.POST['url']!='':
                        error='SOLO ADMINTE UN TIPO DE PREGUNTA'
                        return render(request,'admin/actualizar_pregunta.html',{'error':error})
                    else:
                        pregunta.question_url=request.POST['url']
                        pregunta.question=POST['pregunta'] 
                        pregunta.resp1=request.POST['resp1']
                        pregunta.resp2=request.POST['resp2']
                        pregunta.resp3=request.POST['resp3']
                        pregunta.resp4=request.POST['resp4']
                        pregunta.correct=request.POST['correcta']
                        pregunta.module_id=request.POST['modulo']
                        pregunta.save()
                        error="LA PREGUNTA SE ACTUALIZÓ"                   
                    return render(request,'admin/actualizar_pregunta.html',{'error':error})

                except:
                    error='LA PREGUNTA NO EXISTE'
                    return render(request,'admin/actualizar_pregunta.html',{'error':error})            
                return render(request,'admin/actualizar_pregunta.html',{'error':error})                
        else:
            return redirect('examen')
    else:
        return redirect('inicio')

def eliminarusuario(request):
    if request.user.is_authenticated:
        user=request.user.is_superuser
        if user == True:
            if request.method=='GET':
                return render(request, 'admin/eliminar_usuario.html')
            else:       
                try:
                    usuario=User.objects.get(username=request.POST['val'])
                    usuario.delete()
                    error="EL USUARIO FUE ELIMININADO"  
                    return render(request,'admin/eliminar_usuario.html',{'error':error})

                except:
                    error='ESTE USUARIO NO EXISTE'
                    return render(request,'admin/eliminar_usuario.html',{'error':error})            
                return render(request,'admin/eliminar_usuario.html',{'error':error})                
        else:
            return redirect('examen')
    else:
        return redirect('inicio')

def eliminarpregunta(request):
    if request.user.is_authenticated:
        user=request.user.is_superuser
        if user == True:
            if request.method=='GET':
                return render(request, 'admin/eliminar_pregunta.html')
            else:       
                try:
                    pregunta=User.objects.get(id=request.POST['val'])
                    pregunta.delete()
                    error="LA PREGUNTA FUE ELIMINADA CORRECTAMENTE"  
                    return render(request,'admin/eliminar_pregunta.html',{'error':error})

                except:
                    error='ESTE USUARIO NO EXISTE'
                    return render(request,'admin/eliminar_pregunta.html',{'error':error})            
                return render(request,'admin/eliminar_pregunta.html',{'error':error})                
        else:
            return redirect('examen')
    else:
        return redirect('inicio')
    



