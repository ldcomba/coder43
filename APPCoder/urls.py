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
    path("eliminarProfesor/<id>", eliminarProfesor, name="eliminarProfesor"),
    path("profesorEditar/<id>", profesorEditar, name="profesorEditar"),
    path("estudiante/list/", EstudianteList.as_view(), name="EstudianteList"),
    path("estudiante/nuevo/", EstudianteCreacion.as_view(), name="EstudianteCrear"),
    path("estudiante/<pk>", EstudianteDetalle.as_view(), name="estudiante_detalle"),
    path("estudiante/borrar/<pk>", EstudianteDelete.as_view(), name="estudiante_borrar"),
    path("estudiante/editar/<pk>", EstudianteUpdate.as_view(), name="estudiante_editar"),

]