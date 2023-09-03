from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Curso(models.Model):
    nombre=models.CharField(max_length=50)
    comision=models.IntegerField()
    def __str__(self):
        return f"{self.nombre} - {self.comision}"
    
class Estudiante(models.Model):
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    email=models.EmailField()
    def __str__(self):
        return f"{self.id} - {self.nombre} - {self.apellido}- {self.email}"
    
class Profesor(models.Model):
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    email=models.EmailField()
    profesion=models.CharField(max_length=30)
    def __str__(self):
        return f"{self.nombre} - {self.apellido}"

class Entregable(models.Model):
    nombre=models.CharField(max_length=30)
    fechaDeEntrega= models.DateField()
    entregado= models.BooleanField()

class Avatar(models.Model):
    #vinculo con el usuario
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    #subcarpeta avatares de media
    imagen=models.ImageField(upload_to="avatars",null=True, blank=True)
