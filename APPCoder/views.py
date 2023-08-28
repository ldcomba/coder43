from django.shortcuts import render
from .models import Curso, Profesor, Estudiante   
from django.http import HttpResponse
from .forms import CursoForm, ProfesorForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


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
            mensaje="Profesor creado"
            
        else:
            mensaje="Datos Invalidos"
        profesores=Profesor.objects.all()
        formulario_profesor=ProfesorForm()
        return render(request,"profesores.html", {"mensaje": mensaje,"formulario":formulario_profesor,"profesores":profesores})
    else:
        formulario_profesor=ProfesorForm()
        profesores=Profesor.objects.all()
        return render(request,"profesores.html",{"formulario":formulario_profesor,"profesores":profesores})
    
def eliminarProfesor(request,id):
    profesor=Profesor.objects.get(id=id)
    profesor.delete()
    formulario_profesor=ProfesorForm()
    profesores=Profesor.objects.all()
    mensaje="Profesor eliminado"
    return render(request,"profesores.html", {"mensaje": mensaje,"formulario":formulario_profesor,"profesores":profesores})

def profesorEditar(request,id):
    profesor=Profesor.objects.get(id=id)
    if request.method=="POST":
        form=ProfesorForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            profesor.nombre=info["nombre"]
            profesor.apellido=info["apellido"]
            profesor.email=info["email"]
            profesor.profesion=info["profesion"]
            profesor.save()

            mensaje="Profesor Editado"
            formulario_profesor=ProfesorForm()
            profesores=Profesor.objects.all()
            return render(request,"profesores.html", {"mensaje": mensaje,"formulario":formulario_profesor,"profesores":profesores})
    else:
        
        formulario_profesor=ProfesorForm(initial={"nombre":profesor.nombre, "apellido":profesor.apellido,"email":profesor.email,"profesion":profesor.profesion})
        return render(request,"profesorEditar.html", {"formulario":formulario_profesor,"profesor":profesor})


class EstudianteList(ListView):
    model= Estudiante
    template_name="estudiantes.html"

class EstudianteCreacion(CreateView):
    model= Estudiante
    success_url= reverse_lazy("EstudianteList")
    fields=['nombre','apellido','email']

class EstudianteDetalle(DetailView):
    model= Estudiante
    template_name="estudiante_detalle.html"


class EstudianteDelete(DeleteView):
    model= Estudiante
    success_url= reverse_lazy("EstudianteList")


class EstudianteUpdate(UpdateView):
    model= Estudiante
    success_url= reverse_lazy("EstudianteList")
    fields=['nombre','apellido','email']



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
