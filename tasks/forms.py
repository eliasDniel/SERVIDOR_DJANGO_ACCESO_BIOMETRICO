from django import forms

from .models import Task,Cliente, Membresia
class TasksForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','important']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Write a title'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Write a description'}),
            'important':forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre','correo','telefono','genero']
        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Write your name'}),
            'correo':forms.EmailInput(attrs={'class':'form-control','placeholder':'Write your email'}),
            'telefono':forms.TextInput(attrs={'class':'form-control','placeholder':'Write your phone'}),
            'genero':forms.Select(attrs={'class':'form-control'}),
        }
        

class MembresiaForm(forms.ModelForm):
    class Meta:
        model = Membresia
        fields = ['tipo', 'precio', 'fecha_inicio', 'fecha_fin', 'estado', 'cliente']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),  # Select para opciones de tipo
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),  # Input numérico
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # Calendario para fecha
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # Calendario para fecha
            'estado': forms.Select(attrs={'class': 'form-control'}),  # Select para opciones de estado
            'cliente': forms.Select(attrs={'class': 'form-control'}),  # Select para elegir cliente
        }
