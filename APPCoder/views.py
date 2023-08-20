from django.shortcuts import render
from .models import Curso, Profesor   
from django.http import HttpResponse
from .forms import CursoForm, ProfesorForm

# Create your views here.
def crear_curso(request):
    nombre_curso="Programación basica"
    comision_curso=9090
    print("Creando curso")  
    curso=Curso(nombre=nombre_curso,comision=comision_curso)
    curso.save()
    respuesta=f"Curso creado: {curso.nombre} - {curso.comision}"
    return HttpResponse(respuesta)

def Listar_cursos(request):   #Listar cusos sin usar template
    cursos=Curso.objects.all()
    respuesta=""
    for curso in cursos:
        respuesta+=f"{curso.nombre} - {curso.comision} <br>"
    return HttpResponse(respuesta)

def inicio (request):
    return render(request,"inicio.html")

def cursos (request):
    cursos=Curso.objects.all()
    return render(request,"cursos.html",{"cursos":cursos})


def profesores(request):
    if request.method=="POST":
        form=ProfesorForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            nombre=info["nombre"]
            apellido=info["apellido"]
            email=info["email"]
            profesion=info["profesion"]
            profesor=Profesor(nombre=nombre,apellido=apellido,email=email,profesion=profesion)
            profesor.save()
            formulario_profesor=ProfesorForm()
            return render(request,"profesores.html", {"mensaje": "Profesor creado","formulario":formulario_profesor})
        else:
            formulario_profesor=ProfesorForm()
            return render(request,"profesores.html", {"mensaje": "Datos Invalidos","formulario":formulario_profesor})
    else:
        formulario_profesor=ProfesorForm()
        ##profesores=Profesor.objects.all()
        return render(request,"profesores.html",{"formulario":formulario_profesor})

def cursoFormulario(request):
    if request.method=="POST":
        ##nombre=request.POST["nombre"]
        ##comision=request.POST["comision"]
        form=CursoForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            nombre=info["nombre"]
            comision=info["comision"]
            curso=Curso(nombre=nombre,comision=comision)
            curso.save()
            return render(request,"cursoFormulario.html",{"mensaje":"Curso creado"})
        return render(request,"cursoFormulario.html",{"mensaje":"Datos invalidos"})
    else:
        formulario_curso= CursoForm()
        return render(request,"cursoFormulario.html", {"formulario":formulario_curso})

def estudiantes (request):
    return render(request,"estudiantes.html")

def entregables(request):
    return render(request,"entregables.html")

def busquedaComison(request):
    return render(request,"busquedaComision.html")

def buscar(request):
    #buscare los datos
    comision=request.GET["comision"]
    if comision!="":
        cursos=Curso.objects.filter(comision__icontains=comision)
        return render(request, "resultadosBusqueda.html", {"cursos": cursos})
    else:
        return render(request,"busquedaComision.html",{"mensaje":"Che no ingresaste nada"})
