from django.shortcuts import render
from .models import Curso, Profesor, Estudiante   
from django.http import HttpResponse
from .forms import CursoForm, ProfesorForm, RegistroUsuarioForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.contrib.auth.mixins import LoginRequiredMixin # para vistas basadas en class
from django.contrib.auth.decorators import login_required # para vistas basadas en Def


# Create your views here.
@login_required
def crear_curso(request):
    nombre_curso="Programación basica"
    comision_curso=9090
    print("Creando curso")  
    curso=Curso(nombre=nombre_curso,comision=comision_curso)
    curso.save()
    respuesta=f"Curso creado: {curso.nombre} - {curso.comision}"
    return HttpResponse(respuesta)

@login_required
def Listar_cursos(request):   #Listar cusos sin usar template
    cursos=Curso.objects.all()
    respuesta=""
    for curso in cursos:
        respuesta+=f"{curso.nombre} - {curso.comision} <br>"
    return HttpResponse(respuesta)

def inicio (request):
    return render(request,"inicio.html")

@login_required
def cursos (request):
    cursos=Curso.objects.all()
    return render(request,"cursos.html",{"cursos":cursos})

@login_required # para vistas basadas en Def
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
    
@login_required    
def eliminarProfesor(request,id):
    profesor=Profesor.objects.get(id=id)
    profesor.delete()
    formulario_profesor=ProfesorForm()
    profesores=Profesor.objects.all()
    mensaje="Profesor eliminado"
    return render(request,"profesores.html", {"mensaje": mensaje,"formulario":formulario_profesor,"profesores":profesores})

@login_required
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


class EstudianteList(LoginRequiredMixin,ListView):
    model= Estudiante
    template_name="estudiantes.html"

class EstudianteCreacion(LoginRequiredMixin,CreateView):
    model= Estudiante
    success_url= reverse_lazy("EstudianteList")
    fields=['nombre','apellido','email']

class EstudianteDetalle(LoginRequiredMixin,DetailView):
    model= Estudiante
    template_name="estudiante_detalle.html"


class EstudianteDelete(LoginRequiredMixin,DeleteView):
    model= Estudiante
    success_url= reverse_lazy("EstudianteList")


class EstudianteUpdate(LoginRequiredMixin,UpdateView):
    model= Estudiante
    success_url= reverse_lazy("EstudianteList")
    fields=['nombre','apellido','email']


@login_required
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




@login_required
def estudiantes (request):
    return render(request,"estudiantes.html")

@login_required
def entregables( request):
    return render(request,"entregables.html")

@login_required
def busquedaComison(request):
    return render(request,"busquedaComision.html")

@login_required
def buscar(request):
    #buscare los datos
    comision=request.GET["comision"]
    if comision!="":
        cursos=Curso.objects.filter(comision__icontains=comision)
        return render(request, "resultadosBusqueda.html", {"cursos": cursos})
    else:
        return render(request,"busquedaComision.html",{"mensaje":"Che no ingresaste nada"})


def login_request(request):
    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            info=form.cleaned_data
            usu=info["username"]
            clave=info["password"]
            usuario=authenticate(username=usu, password=clave)
            if usuario is not None:
                login(request, usuario)
                return render(request, "inicio.html", {"mensaje":f"Usuario {usu} logueado correctamente"})
            else:
                return render(request, "login.html", {"form":form, "mensaje":"Datos Invalidos"})
        else:
            return render(request, "login.html", {"form":form, "mensaje":"Datos Invalidos"})
    else:
        form=AuthenticationForm()
        return render(request, "login.html", {"form":form})
    
def register(request):
        if request.method == 'POST':
            form = RegistroUsuarioForm(request.POST)
            if form.is_valid():
                username=form.cleaned_data['username']
                form.save()
                return render(request, "inicio.html", {"mensaje":"Usuario Creado :)"})
            
            else:
                form=RegistroUsuarioForm()
                return render(request,"register.html", {"form":form,"mensaje":"Datos invalidos"})
        else:
            form=RegistroUsuarioForm()
        return render(request,"register.html", {"form":form})
