from django import forms
from .models import Task, Cliente, Membresia

class TasksForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a title', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a description', 'required': True}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'correo', 'telefono', 'genero']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your name', 'required': True}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Write your email', 'required': True}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write your phone', 'required': True}),
            'genero': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }

class MembresiaForm(forms.ModelForm):
    class Meta:
        model = Membresia
        fields = ['tipo', 'precio', 'fecha_inicio', 'fecha_fin', 'estado', 'cliente']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control', 'required': True}),  # Select para opciones de tipo
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio', 'required': True}),  # Input numérico
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),  # Calendario para fecha
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),  # Calendario para fecha
            'estado': forms.Select(attrs={'class': 'form-control', 'required': True}),  # Select para opciones de estado
            'cliente': forms.Select(attrs={'class': 'form-control', 'required': True}),  # Select para elegir cliente
        }
