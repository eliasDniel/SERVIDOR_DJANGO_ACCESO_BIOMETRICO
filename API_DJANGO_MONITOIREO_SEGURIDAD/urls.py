"""
URL configuration for admin_gimnasio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_seguridad_acceso_biometrico import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/verificar_acceso/', views.api_verificar_acceso, name='api_verificar_acceso'),
    path('api/usuarios/', views.api_lista_entradas, name='api_lista_usuarios'),
    path('api/users/', views.api_lista_users, name='api_lista_users'),
    path('api/create_user/', views.api_create_user, name='create_user'), 
    path('api/metrica_ingresos/', views.api_metrica_ingresos, name='api_metrica_ingresos'),
    path('api/save-device-token/', views.api_save_device_token, name='save_device_token'),
]
