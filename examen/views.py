from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from administrador.models import *

# Create your views here.
@login_required
def examen(request):
    exam=ExamenesExam.objects.all()
    return render(request ,'exam/welcome.html')
   

@login_required
def modulo(request, id_mod):
    if id_mod > 4:
        return redirect('examen')
    else:
        usuario = request.user
        # Obtenemos el examen del user
        examen = usuario.examenesexam_set.get()
        # Validamos que el módulo esté activo
        if id_mod == 1:
            status_module = examen.status_mod_1
        elif id_mod == 2:
            status_module = examen.status_mod_2
        elif id_mod == 3:
            status_module = examen.status_mod_3
        elif id_mod == 4:
            status_module = examen.status_mod_4
        
        if status_module:
            # Obtenemos las preguntas del modulo y usuario
            desgloce = examen.examenesbreakdown_set.filter(question__module__id=id_mod)

            # Creamos una lista de ids por modulo
            desgloce_ids = []
            for item in desgloce:
                desgloce_ids.append(item.id)
            request.session[f'modulo-{ id_mod }'] = desgloce_ids

            return redirect('question', id_mod=id_mod, id_ques=1)
        else:
            return redirect('examen')

@login_required
def question(request, id_mod, id_ques):
    # Procesos con GET
    if request.method == 'GET':
        current_list_question = request.session.get(f'modulo-{ id_mod }')
        if id_ques < len(current_list_question) :
            # Obtenemos datos de Pregunta
            # id_question Viene de Examen
            if id_mod==1:
                mod_name='Pensamiento Analítico'
            elif id_mod==2:
                mod_name='Estructura de la lengua'
            elif id_mod==3:
                mod_name="Comprensión lectora"
            else:
                mod_name="Pensamiento matemáttico"
            id_question_exam = current_list_question[id_ques - 1]
            question_in_exam = ExamenesBreakdown.objects.get(pk=id_question_exam)
            respuesta = question_in_exam.answer
            question_in_question = PreguntasQuestion.objects.get(pk=question_in_exam.question.id)
            return render(request, 'exam/question.html', 
                        {"question": question_in_question, 
                        "pregunta": id_ques,
                        "respuesta": respuesta,
                        "question_in_breakdown": question_in_exam.id,
                        "id_mod": id_mod,
                        "mod_name":mod_name,
                        "siguiente": id_ques + 1})
        else:
            return redirect('save_modulo', id_mod=id_mod)
    # Procesos con POST
    if request.method == 'POST':
        respuesta = request.POST['respuesta']
        id_question_exam = request.POST['question_in_breakdown']
        question_in_exam = ExamenesBreakdown.objects.get(pk=id_question_exam)
        # Update de Object
        if respuesta != '-':
            question_in_exam.answer = respuesta
            question_in_exam.save()

        return redirect('question', id_mod=id_mod, id_ques=id_ques)
    
@login_required
def save_modulo(request, id_mod):
    if request.method == 'GET':
        return render(request, 'exam/save_modulo.html', {"id_mod": id_mod})
    
    if request.method == 'POST':
        user = request.user
        # Obtenemos el examen del user
        examen = user.examenesexam_set.get()
        if id_mod == 1:
            examen.status_mod_1 = False
            resultado = examen.get_results(id_mod)
            examen.result_mod_1 = resultado
        elif id_mod == 2:
            examen.status_mod_2 = False
            resultado = examen.get_results(id_mod)
            examen.result_mod_2 = resultado
        elif id_mod == 3:
            examen.status_mod_3 = False
            resultado = examen.get_results(id_mod)
            examen.result_mod_3 = resultado
        elif id_mod == 4:
            examen.status_mod_4 = False
            resultado = examen.get_results(id_mod)
            examen.result_mod_4 = resultado
        examen.average=(examen.result_mod_1+examen.result_mod_2+examen.result_mod_3+examen.result_mod_4)/4
        examen.save()
        return redirect('examen')

