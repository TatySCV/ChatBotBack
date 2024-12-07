import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import transaction

from .Integration import Integration


from aplicacion.models import Conversacion, Mensaje, Usuario


def listar_conversaciones(request):
    user_data = request.GET.get("user")

    user_dict = json.loads(user_data) if user_data else {}

    user_id = user_dict.get("id")
    # Obtener el usuario
    usuario = Usuario.objects.get(id=user_id)

    # Obtener conversaciones del usuario
    conversaciones = Conversacion.objects.filter(usuario=usuario).prefetch_related(
        "mensajes"
    )

    # Serializar datos
    conversaciones_serializadas = [
        {
            "id": conversacion.id,
            "usuario": conversacion.usuario.id,
            "titulo": conversacion.titulo,
            "fecha_creacion": conversacion.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for conversacion in conversaciones
    ]

    # Retornar las conversaciones serializadas
    return JsonResponse(conversaciones_serializadas, safe=False, status=200)

@csrf_exempt
def mensajes(request):
    print("VISTA MENSAJES")  # Para diagnóstico
    if request.method == "POST":
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = json.loads(request.body)

            id_conversacion = data.get("id")
            id_usuario = data.get("user")

            # Convertir los parámetros a enteros
            id_conversacion = int(id_conversacion)
            id_usuario = int(id_usuario)

            # Intentar obtener la conversación existente
            try:
                conversacion = Conversacion.objects.get(pk=id_conversacion)
            except Conversacion.DoesNotExist:
                return JsonResponse(
                    {
                        "error": f"No se encontró la conversación con id {id_conversacion}."
                    },
                    status=404,
                )

            # Obtener todos los mensajes asociados
            mensajes = conversacion.mensajes.all()

            # Serializar la conversación y los mensajes
            conversacion_serializada = {
                "id": conversacion.id,
                "usuario": conversacion.usuario.id,
                "titulo": conversacion.titulo,
                "fecha_creacion": conversacion.fecha_creacion.strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),
                "mensajes": [
                    {
                        "id": mensaje.id,
                        "usuario": mensaje.usuario.id,
                        "remitente": mensaje.remitente,
                        "contenido": mensaje.contenido,
                        "timestamp": mensaje.timestamp.strftime("%d-%m-%Y %H:%M:%S"),
                        "contexto": mensaje.contexto,
                    }
                    for mensaje in mensajes
                ],
            }

            # Responder con la conversación serializada
            return JsonResponse(conversacion_serializada, safe=False, status=200)

        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "El cuerpo de la solicitud no es válido."},
                status=400,
            )
        except Exception as e:
            print(f"Error inesperado: {str(e)}")  # Para diagnóstico
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido."}, status=405)


@csrf_exempt
def respuesta_chatbot(request):
    print("EN VISTA DE RESPUESTA CHATBOT")  # Para diagnóstico
    if request.method == "POST":
        try:
            # Obtener los datos enviados desde el frontend
            data = json.loads(request.body)

            mensaje = data.get("mensaje", "").strip()
            id_conversacion = int(data.get("id_conversacion", 0))  # Convertir a entero
            titulo_conversacion = data.get("titulo_conversacion", "").strip()
            id_usuario = data.get("user")  # Obtener id_usuario de los datos enviados

            print(f"ID de conversación recibido: {id_conversacion}")

            # Verificar que el mensaje no esté vacío
            if not mensaje:
                return JsonResponse(
                    {"error": "El mensaje no puede estar vacío."}, status=400
                )

            with transaction.atomic():  # Garantizar atomicidad
                if id_conversacion == 0:
                    # Crear nueva conversación
                    usuario = Usuario.objects.get(id=id_usuario)
                    conversacion = Conversacion(
                        usuario=usuario,
                        titulo=titulo_conversacion or "Conversación con el bot",
                        fecha_creacion=timezone.now(),
                    )
                    conversacion.save()

                    # Crear y asociar el mensaje inicial
                    mensaje_usuario = Mensaje(
                        contenido=mensaje,
                        remitente="usuario",
                        usuario=usuario,
                        timestamp=timezone.now(),
                    )
                    mensaje_usuario.save()
                    conversacion.mensajes.add(mensaje_usuario)
                else:
                    # Agregar mensaje a una conversación existente
                    try:
                        conversacion = Conversacion.objects.get(pk=id_conversacion)
                    except Conversacion.DoesNotExist:
                        return JsonResponse(
                            {"error": "Conversación no encontrada."}, status=404
                        )

                    mensaje_usuario = Mensaje(
                        contenido=mensaje,
                        remitente="usuario",
                        usuario=conversacion.usuario,
                        timestamp=timezone.now(),
                    )
                    mensaje_usuario.save()
                    conversacion.mensajes.add(mensaje_usuario)

                # Obtener el contexto de mensajes (últimos mensajes en orden inverso)
                context = conversacion.mensajes.order_by("-timestamp").values(
                    "contenido", "remitente"
                )

                # Generar respuesta del bot
                bot = Integration()
                respuesta_generada = bot.obtener_respuesta(mensaje, context)

                # Guardar el mensaje del bot
                mensaje_bot = Mensaje(
                    contenido=respuesta_generada,
                    remitente="bot",
                    usuario=conversacion.usuario,
                    timestamp=timezone.now(),
                )
                mensaje_bot.save()
                conversacion.mensajes.add(mensaje_bot)

                # Guardar conversación actualizada
                conversacion.save()

            # Respuesta al frontend
            return JsonResponse(
                {
                    "id_conversacion": conversacion.id,
                    "respuesta_bot": respuesta_generada,
                },
                status=200,
            )

        except Usuario.DoesNotExist:
            print("Error: Usuario no encontrado.")
            return JsonResponse({"error": "El usuario no existe."}, status=404)

        except Exception as e:
            print(f"Error: {str(e)}")  # Imprimir el error para depuración
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def nueva_conversacion(request):
    user_data = request.GET.get("user")
    
    user_dict = json.loads(user_data) if user_data else {}

    user_id = user_dict.get("id")
    # Obtener el usuario
    usuario = Usuario.objects.get(id=user_id)
    
    # Crear nueva conversación
    conversacion = Conversacion(
        usuario=usuario,
        titulo="Conversación con el bot",
        fecha_creacion=timezone.now(),
    )
    
    conversacion.save()
    
    # Serializar datos
    conversacion_serializada = {
        "id": conversacion.id,
        "usuario": conversacion.usuario.id,
        "titulo": conversacion.titulo,
        "fecha_creacion": conversacion.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    # Retornar la conversación serializada
    return JsonResponse(conversacion_serializada, status=200, safe=False)
