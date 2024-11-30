import json
import jwt
import datetime
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from functools import wraps
from django.conf import settings

def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        if token is None:
            return JsonResponse({'error': 'Token no proporcionado'}, status=401)

        try:
            token = token.split()[1]  # Remueve el prefijo "Bearer"
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
            request.user_id = payload['user_id']  # Guarda el user_id en la solicitud
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return JsonResponse({'error': 'Token inválido o expirado'}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view

@csrf_exempt
def login(request):
    print("Vista de login: Inicio")

    print(f'Método: {request.method}')
        
    if request.method == 'POST':
        print("Método POST recibido.")
        
        try:
            # Deserializar el cuerpo de la solicitud JSON
            data = json.loads(request.body)  # Cambiado para obtener el body
            username = data.get('username')  # Obtén el username
            password = data.get('password')  # Obtén la contraseña
            
            print(f'Usuario: {username}')  # Imprimir el nombre de usuario
            print(f'Contraseña: {password}')  # Imprimir la contraseña

            # Autenticar el usuario
            user = authenticate(username=username, password=password)
            
            if user is not None:
                print("Autenticación exitosa.")
                
            # Si la autenticación es exitosa, generar el token JWT
                payload = {
                    'user_id': user.id,
                    'username': user.username,  # Agregar rol al payload
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
                    'iat': datetime.datetime.utcnow(),
                }
                token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
                
                # Preparar el objeto usuario para la respuesta
                usuario_info = {
                    'id': user.id,
                    'username': user.username,
                }

                print("Token JWT generado.")
                return JsonResponse({'token': token, 'usuario': usuario_info}, status=200)  # Devuelve el token y el objeto usuario
            else:
                print("Credenciales inválidas.")
                return JsonResponse({'error': 'Credenciales inválidas'}, status=401)

        except json.JSONDecodeError:
            print("Error: JSON mal formado.")
            return JsonResponse({'error': 'JSON mal formado'}, status=400)

    print("Método no permitido.")
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def logout_sesion(request):
    print(f'Vista de Logout: Inicio')
    
    if request.method == 'POST':
        print("Método POST recibido.")
        
        try:
            # Deserializar el cuerpo de la solicitud JSON
            data = json.loads(request.body)  # Cambiado para obtener el body
            user = data.get('user')  # Obtén el username
            
            if user:
                
                # Obtener el token de autorización
                auth_header = request.headers.get('Authorization')
                if auth_header is None:
                    return JsonResponse({'error': 'Token no proporcionado'}, status=400)

                token = auth_header.split(' ')[1]  # Extrae el token del encabezado
                print("JWT:", token)  # Imprimir el JWT en la consola
                
                print("Usuario:", user)  # Imprimir el usuario en la consola
              
                logout(request)
            
            return JsonResponse({'message': 'Logout exitoso'}, status=200)
            
        except json.JSONDecodeError:
            print("Error: JSON mal formado.")
            return JsonResponse({'error': 'JSON mal formado'}, status=400)

    print("Método no permitido.")
    return JsonResponse({'error': 'Método no permitido'}, status=405)    