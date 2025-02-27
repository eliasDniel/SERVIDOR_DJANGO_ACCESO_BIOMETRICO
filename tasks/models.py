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
# class Cliente(models.Model):
#     nombre = models.CharField(max_length=100)
#     correo = models.EmailField(unique=True)
#     telefono = models.CharField(max_length=15, blank=True, null=True)
#     creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="clientes_creados")
#     modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="clientes_modificados")
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     fecha_modificacion = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.nombre


# class Membresia(models.Model):
#     TIPO_MEMBRESIA_CHOICES = [
#         ('Básica', 'Básica'),
#         ('Premium', 'Premium'),
#         ('VIP', 'VIP'),
#         ('Estudiante', 'Estudiante'),
#         ('Familiar', 'Familiar'),
#     ]

#     tipo = models.CharField(max_length=50, choices=TIPO_MEMBRESIA_CHOICES)
#     precio = models.DecimalField(max_digits=8, decimal_places=2)
#     descripcion = models.TextField(blank=True, null=True)
#     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="membresias")
#     fecha_inicio = models.DateField()
#     fecha_fin = models.DateField()
#     creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="membresias_creadas")
#     modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="membresias_modificadas")
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     fecha_modificacion = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.tipo} ({self.fecha_inicio} - {self.fecha_fin})"

#     def esta_activa(self):
#         """Retorna True si la membresía está activa, basado en la fecha actual."""
#         hoy = date.today()
#         return self.fecha_inicio <= hoy <= self.fecha_fin

#     def dias_restantes(self):
#         """Calcula los días restantes hasta la fecha de fin."""
#         hoy = date.today()
#         if hoy > self.fecha_fin:
#             return 0
#         return (self.fecha_fin - hoy).days


# class Pago(models.Model):
#     METODO_PAGO_CHOICES = [
#         ('Efectivo', 'Efectivo'),
#         ('Tarjeta', 'Tarjeta'),
#         ('Transferencia', 'Transferencia'),
#         ('Paypal', 'Paypal'),
#     ]

#     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="pagos")
#     fecha = models.DateField(auto_now_add=True)
#     monto = models.DecimalField(max_digits=8, decimal_places=2)
#     metodo_pago = models.CharField(max_length=50, choices=METODO_PAGO_CHOICES)
#     creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="pagos_creados")
#     modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="pagos_modificados")
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     fecha_modificacion = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Pago de {self.cliente.nombre} - ${self.monto} ({self.metodo_pago})"
