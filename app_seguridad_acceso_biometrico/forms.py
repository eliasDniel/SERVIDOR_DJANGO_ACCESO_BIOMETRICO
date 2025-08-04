from django import forms
# from .models import UsuarioHuella


# class UsuarioHuellaForm(forms.ModelForm):
#     class Meta:
#         model = UsuarioHuella
#         fields = ['nombre', 'email', 'telefono', 'activo', 'huella_id']
#         widgets = {
#             'nombre': forms.TextInput(attrs={
#                 'class': 'form-control', 
#                 'placeholder': 'Escribe tu nombre', 
#                 'required': True
#             }),
#             'email': forms.EmailInput(attrs={
#                 'class': 'form-control', 
#                 'placeholder': 'Escribe tu correo electrónico', 
#                 'required': True
#             }),
#             'telefono': forms.TextInput(attrs={
#                 'class': 'form-control', 
#                 'placeholder': 'Escribe tu número de teléfono', 
#                 'required': False
#             }),
#             'activo': forms.CheckboxInput(attrs={
#                 'class': 'form-check-input',
#             }),
#             'huella_id': forms.Textarea(attrs={
#                 'class': 'form-control', 
#                 'placeholder': 'Pega aquí la huella en Base64', 
#                 'rows': 3, 
#                 'required': False
#             }),
#         }
