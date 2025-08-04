import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from app_seguridad_acceso_biometrico.utils import send_push_notification_v1
from .models import RegistroEntrada,Device
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone  # Asegúrate de importar esto correctamente
from django.contrib.auth.hashers import make_password

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@csrf_exempt
def api_verificar_acceso(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            channel_layer = get_channel_layer()

            if 'username' in data and 'password' in data:
                user = authenticate(username=data['username'], password=data['password'])
                if user:
                    RegistroEntrada.objects.create(usuario=user, metodo='PIN')
                    device = Device.objects.first()
                    # ✉️ Enviar notificación FCM
                    title = "Se registro una entrada justo ahora!"
                    body = f"{user.first_name} {user.last_name}, ha ingresado por el metodo de PIN."
                    send_push_notification_v1(device.token, title, body)
                    async_to_sync(channel_layer.group_send)(
                        "accesos",
                        {
                            "type": "enviar_acceso",
                            "data": {
                                "usuario__username": user.username,
                                "usuario__first_name": user.first_name,
                                "usuario__last_name": user.last_name,
                                "usuario__email": user.email,
                                "usuario__is_active": user.is_active,
                                "usuario__is_staff": user.is_staff,
                                "fecha_hora": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                                "metodo": "PIN",
                                "status": "OK"
                            }
                        }
                    )
                    return JsonResponse({'status': 'OK'})
                else:
                    return JsonResponse({'status': 'DENEGADO'})

            elif 'huella_id' in data:
                try:
                    user = get_object_or_404(User, pk=data['huella_id'])
                    RegistroEntrada.objects.create(usuario=user, metodo='Huella Digital')
                    device = Device.objects.first()
                    # ✉️ Enviar notificación FCM
                    title = "Se registro una entrada justo ahora!"
                    body = f"{user.first_name} {user.last_name}, ha ingresado por el metodo de Huella Digital."
                    send_push_notification_v1(device.token, title, body)

                    # Emitir evento
                    async_to_sync(channel_layer.group_send)(
                        "accesos",
                        {
                            "type": "enviar_acceso",
                            "data": {
                                "usuario__username": user.username,
                                "usuario__first_name": user.first_name,
                                "usuario__last_name": user.last_name,
                                "usuario__email": user.email,
                                "usuario__is_active": user.is_active,
                                "usuario__is_staff": user.is_staff,
                                "fecha_hora": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                                "metodo": "Huella Digital",
                                "status": "OK"
                            }
                        }
                    )

                    return JsonResponse({'status': 'OK'})
                except:
                    return JsonResponse({'status': 'DENEGADO'})

            else:
                return JsonResponse({'status': 'ERROR', 'message': 'Datos incompletos'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'ERROR', 'message': 'JSON inválido'}, status=400)

    return JsonResponse({'status': 'ERROR', 'message': 'Método no permitido'}, status=405)

@csrf_exempt
def api_lista_entradas(request):
    if request.method == 'GET':
        registros_entradas = RegistroEntrada.objects.all().values(
        'usuario', 
        'usuario__username', 
        'usuario__first_name', 
        'usuario__last_name', 
        'usuario__email', 
        'usuario__is_active', 
        'usuario__is_staff', 
        'metodo', 
        'fecha_hora'
        )
        registros_entradas_list = list(registros_entradas)
        return JsonResponse({'registros_entradas': registros_entradas_list}, safe=False)

    return JsonResponse({'status': 'ERROR', 'message': 'Método no permitido'}, status=405)       


@csrf_exempt
def api_lista_users(request):
    if request.method == 'GET':
        users = User.objects.all().values( 
        'username', 
        'first_name', 
        'last_name', 
        'email', 
        'is_active', 
        'is_staff', 
        )
        user_list = list(users)
        return JsonResponse({'users': user_list}, safe=False)

    return JsonResponse({'status': 'ERROR', 'message': 'Método no permitido'}, status=405)       



@csrf_exempt
def api_create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            required_fields = ['username', 'first_name', 'last_name', 'email', 'password']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'status': 'ERROR', 'message': f'{field} is required'}, status=400)

            username = data['username']
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            password = data['password']
            
            is_active = data.get('is_active', True)
            is_staff = data.get('is_staff', False)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'ERROR', 'message': 'El nombre de usuario ya existe'}, status=400)
            
            

            user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=make_password(password),
                is_active=is_active,
                is_staff=is_staff
            )
            user.save()

            

            response_data = {
                'status': 'OK',
                'message': 'Usuario creado exitosamente',
                'user': {
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                }
            }

            return JsonResponse(response_data, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'ERROR', 'message': 'JSON inválido'}, status=400)

        except Exception as e:
            return JsonResponse({'status': 'ERROR', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'ERROR', 'message': 'Método no permitido'}, status=405)



@csrf_exempt
def api_metrica_ingresos(request):
    if request.method == 'GET':
        # Fecha actual (solo el día)
        today = timezone.now().date()

        # Contar los registros de entrada del día
        registros_entrada_dia = RegistroEntrada.objects.filter(fecha_hora__date=today).count()

        # Contar el total de usuarios
        total_usuarios = User.objects.count()

        # Contar los usuarios activos e inactivos
        usuarios_activos = User.objects.filter(is_staff=True).count()
        usuarios_inactivos = User.objects.filter(is_staff=False).count()

        # Contar los registros por huella y PIN
        registros_huella = RegistroEntrada.objects.filter(metodo='Huella Digital', fecha_hora__date=today).count()
        registros_pin = RegistroEntrada.objects.filter(metodo='PIN', fecha_hora__date=today).count()

        # Crear la respuesta JSON
        response_data = {
            'status': 'OK',
            'data': {
                'registros_entrada_dia': registros_entrada_dia,
                'total_usuarios': total_usuarios,
                'usuarios_activos': usuarios_activos,
                'usuarios_inactivos': usuarios_inactivos,
                'registros_huella': registros_huella,
                'registros_pin': registros_pin,
            }
        }

        return JsonResponse(response_data, status=200)

    return JsonResponse({'status': 'ERROR', 'message': 'Método no permitido'}, status=405)


@csrf_exempt
def api_save_device_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['device_token']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'status': 'ERROR', 'message': f'{field} is required'}, status=400)

            device_token = data['device_token']


            # Guardar o actualizar el token para el usuario
            device,created = Device.objects.update_or_create(
                defaults={'token': device_token}
            )

            return JsonResponse({
    'status': 'OK',
    'message': 'Token guardado correctamente',
    
}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'ERROR', 'message': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'ERROR', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'ERROR', 'message': 'Método no permitido'}, status=405)