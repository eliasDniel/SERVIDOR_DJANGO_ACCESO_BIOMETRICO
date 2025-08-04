# SERVIDOR_DJANGO_ACCESO_BIOMETRICO

Este proyecto es un servidor Django para el control y monitoreo de acceso biométrico, ideal para aplicaciones como gimnasios, oficinas o instalaciones que requieren control de acceso seguro y registro de entradas/salidas.

## Características principales
- Autenticación y autorización de usuarios.
- Registro de accesos mediante biometría (huella, rostro, etc.).
- Administración de usuarios y dispositivos desde el panel de Django.
- Notificaciones y monitoreo en tiempo real usando Django Channels.
- Integración con Firebase para notificaciones push (ver carpeta `firebase/`).
- Configuración para despliegue en producción con Whitenoise.

## Estructura del proyecto

```
API_DJANGO_MONITOIREO_SEGURIDAD/   # Configuración principal del proyecto Django
app_seguridad_acceso_biometrico/   # Aplicación principal de control de acceso biométrico
firebase/                          # Configuración de notificaciones push
manage.py                         # Script de gestión de Django
requirements.txt                  # Dependencias del proyecto
build.sh                          # Script de build/despliegue (opcional)
db.sqlite3                        # Base de datos SQLite (desarrollo)
```

## Instalación y ejecución local

1. Clona el repositorio:
   ```
   git clone https://github.com/tu-usuario/tu-repo.git
   cd SERVIDOR_DJANGO_ACCESO_BIOMETRICO
   ```
2. Crea un entorno virtual e instala dependencias:
   ```
   python -m venv venv
   venv\Scripts\activate  # En Windows
   pip install -r requirements.txt
   ```
3. Configura las variables de entorno en un archivo `.env` (opcional, recomendado para producción):
   ```
   SECRET_KEY=tu_clave_secreta
   DB_ENGINE=django.db.backends.postgresql  # O el motor que uses
   DB_DATABASE=nombre_db
   DB_USERNAME=usuario_db
   DB_PASSWORD=contraseña_db
   DB_SOCKET=localhost
   DB_PORT=5432
   ```
4. Realiza las migraciones:
   ```
   python manage.py migrate
   ```
5. Ejecuta el servidor de desarrollo:
   ```
   python manage.py runserver
   ```

## Despliegue en producción
- Configura `DEBUG = False` en `settings.py`.
- Usa Whitenoise para servir archivos estáticos.
- Configura correctamente las variables de entorno y la base de datos.

## Notas adicionales
- El proyecto usa Django Channels para comunicación en tiempo real.
- La integración con Firebase permite notificaciones push (ver `firebase/notifications.json`).
- El archivo `requirements.txt` contiene todas las dependencias necesarias.

## Licencia
Este proyecto es de uso libre para fines educativos y de desarrollo.
