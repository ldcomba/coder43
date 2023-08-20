from django.urls import path
from .views import *

urlpatterns = [
    path('crearCurso/', crear_curso),
    path("listar_curso/", Listar_cursos),
    path("cursos/",cursos, name="cursos"),
    path("profesores/",profesores, name="profesores"),
    path("estudiantes/",estudiantes, name="estudiantes"),
    path("entregables/",entregables, name="entregables"),
    path("cursoFormulario/",cursoFormulario, name="cursoFormulario"),
    path("busquedaComision/", busquedaComison, name="busquedaComision"),
    path("buscar/", buscar, name="buscar"),
]