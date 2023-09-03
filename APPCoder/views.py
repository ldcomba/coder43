from django.shortcuts import render
from .models import Curso, Profesor, Estudiante, Avatar
from django.http import HttpResponse
from .forms import CursoForm, ProfesorForm, RegistroUsuarioForm, UserEditForm, AvatarForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.contrib.auth.mixins import LoginRequiredMixin # para vistas basadas en class
from django.contrib.auth.decorators import login_required # para vistas basadas en Def



def obtenerAvatar(request):
    avatares=Avatar.objects.filter(user=request.user.id)
    if len(avatares)!=0:
        return avatares[0].imagen.url
    else:
        return "media/avatars/avatarpordefecto.png"



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
    #avatar=Avatar.objects.filter(user=request.user.id)[0].imagen.url
    return render(request,"inicio.html",{"avatar":obtenerAvatar(request)})

@login_required
def cursos (request):
    cursos=Curso.objects.all()
    return render(request,"cursos.html",{"cursos":cursos,"avatar":obtenerAvatar(request)})

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
        #avatar=Avatar.objects.filter(user=request.user.id)[0].img.url
        return render(request,"profesores.html", {"mensaje": mensaje,"formulario":formulario_profesor,"profesores":profesores,"avatar":obtenerAvatar(request)})
    else:
        formulario_profesor=ProfesorForm()
        profesores=Profesor.objects.all()
        
        #avatar=Avatar.objects.filter(user=request.user.id)[0].img.url
        return render(request,"profesores.html",{"formulario":formulario_profesor,"profesores":profesores,"profesores":profesores,"avatar":obtenerAvatar(request)})
    
@login_required    
def eliminarProfesor(request,id):
    profesor=Profesor.objects.get(id=id)
    profesor.delete()
    formulario_profesor=ProfesorForm()
    profesores=Profesor.objects.all()
    mensaje="Profesor eliminado"
    return render(request,"profesores.html", {"mensaje": mensaje,"formulario":formulario_profesor,"profesores":profesores,"avatar":obtenerAvatar(request)})

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
            return render(request,"profesores.html", {"mensaje": mensaje,"formulario":formulario_profesor,"profesores":profesores,"avatar":obtenerAvatar(request)})
    else:
        
        formulario_profesor=ProfesorForm(initial={"nombre":profesor.nombre, "apellido":profesor.apellido,"email":profesor.email,"profesion":profesor.profesion,"avatar":obtenerAvatar(request)})
        return render(request,"profesorEditar.html", {"formulario":formulario_profesor,"profesor":profesor,"avatar":obtenerAvatar(request)})


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
            return render(request,"cursoFormulario.html",{"mensaje":"Curso creado","avatar":obtenerAvatar(request)})
        return render(request,"cursoFormulario.html",{"mensaje":"Datos invalidos","avatar":obtenerAvatar(request)})
    else:
        formulario_curso= CursoForm()
        return render(request,"cursoFormulario.html", {"formulario":formulario_curso,"avatar":obtenerAvatar(request)})




@login_required
def estudiantes (request):
    return render(request,"estudiantes.html",{"avatar":obtenerAvatar(request)})

@login_required
def entregables( request):
    return render(request,"entregables.html",{"avatar":obtenerAvatar(request)})

@login_required
def busquedaComison(request):
    return render(request,"busquedaComision.html",{"avatar":obtenerAvatar(request)})

@login_required
def buscar(request):
    #buscare los datos
    comision=request.GET["comision"]
    if comision!="":
        cursos=Curso.objects.filter(comision__icontains=comision)
        return render(request, "resultadosBusqueda.html", {"cursos": cursos,"avatar":obtenerAvatar(request)})
    else:
        return render(request,"busquedaComision.html",{"mensaje":"Che no ingresaste nada","avatar":obtenerAvatar(request)})


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
                return render(request, "inicio.html", {"mensaje":f"Usuario {usu} logueado correctamente","avatar":obtenerAvatar(request)})
            else:
                return render(request, "login.html", {"form":form, "mensaje":"Datos Invalidos","avatar":obtenerAvatar(request)})
        else:
            return render(request, "login.html", {"form":form, "mensaje":"Datos Invalidos","avatar":obtenerAvatar(request)})
    else:
        form=AuthenticationForm()
        return render(request, "login.html", {"form":form,"avatar":obtenerAvatar(request)})
    
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

@login_required
def editarPerfil(request):
    usuario=request.user

    if request.method=="POST":
        form=UserEditForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            usuario.email=info["email"]
            usuario.password1=info["password1"]
            usuario.password2=info["password2"]
            usuario.first_name=info["first_name"]
            usuario.last_name=info["last_name"]
            usuario.save()
            return render(request,"inicio.html",{"mensaje": f"usuario {usuario.username} editado correctamente"})
        else:
            return render(request, "editarPerfil.html", {"form": form, "nombreusuario":usuario.username, "mensaje":"Datos invalidos"})
    else:
        form=UserEditForm(instance=usuario)
        return render(request, "editarPerfil.html", {"form": form, "nombreusuario":usuario.username})        
    
def agregarAvatar(request):
    if request.method=="POST":
        form=AvatarForm(request.POST,request.FILES)
        if form.is_valid():
            avatar=Avatar(user=request.user,imagen=request.FILES["imagen"])
            avatarViejo=Avatar.objects.filter(user=request.user)
            if len(avatarViejo)>0:
                avatarViejo[0].delete()
            avatar.save()
            return render(request, "inicio.html", {"mensaje":f"Avatar agregado correctamente", "avatar":obtenerAvatar(request)})
        else:
            return render(request, "agregarAvatar.html", {"form": form, "usuario": request.user, "mensaje":"Error al agregar el avatar"})
    else:
        form=AvatarForm()
        return render(request, "agregarAvatar.html",{"form":form,"usuario":request.user, "avatar":obtenerAvatar(request)})