from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True,blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' by ' + self.user.username

class Cliente(models.Model):
    GENERO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Membresia(models.Model):
    TIPO_MEMBRESIA_CHOICES = [
        ('Básica', 'Básica'),
        ('Premium', 'Premium'),
        ('VIP', 'VIP'),
        ('Estudiante', 'Estudiante'),
        ('Familiar', 'Familiar'),
    ]
    ESTADO_CHOICES = [
        ('Activa', 'Activa'),
        ('Expirada', 'Expirada'),
        ('Suspendida', 'Suspendida'),
    ]

    tipo = models.CharField(max_length=50, choices=TIPO_MEMBRESIA_CHOICES)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activa')
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="membresias")

    def __str__(self):
        return f"{self.tipo} - {self.cliente.nombre} (Desde {self.fecha_inicio} hasta {self.fecha_fin})"

