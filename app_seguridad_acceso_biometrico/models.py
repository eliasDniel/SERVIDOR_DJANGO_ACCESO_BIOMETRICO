from django.db import models
from django.contrib.auth.models import User

class RegistroEntrada(models.Model):
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='registros_entrada',
        help_text="Usuario asociado a este registro de entrada"
    )
    fecha_hora = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora del registro de entrada")
    metodo = models.CharField(max_length=20, default='desconocido')


    def __str__(self):
        return f"Registro de entrada: {self.usuario.username} en {self.fecha_hora}"
    
    @property
    def fecha_formateada(self):
        return self.fecha_hora.strftime('%d/%m/%Y, %I:%M %p')



class Device(models.Model):
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)