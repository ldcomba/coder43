from django.shortcuts import render
from .models import Curso   
from django.http import HttpResponse

# Create your views here.
def crear_curso(request):
    nombre_curso="Programación basica"
    comision_curso=9090
    print("Creando curso")  
    curso=Curso(nombre=nombre_curso,comision=comision_curso)
    curso.save()
    respuesta=f"Curso creado: {curso.nombre} - {curso.comision}"
    return HttpResponse(respuesta)

def Listar_cursos(request):
    cursos=Curso.objects.all()
    respuesta=""
    for curso in cursos:
        respuesta+=f"{curso.nombre} - {curso.comision} <br>"
    return HttpResponse(respuesta)