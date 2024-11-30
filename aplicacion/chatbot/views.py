import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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


def mensajes(request):
    id_conversacion = request.GET.get("id")

    print(id_conversacion)

    if not id_conversacion:
        return JsonResponse({"error": "El parámetro 'id' es requerido."}, status=400)

    try:
        # Obtener una única conversación
        conversacion = Conversacion.objects.get(pk=id_conversacion)
    except Conversacion.DoesNotExist:
        return JsonResponse({"error": "La conversación no existe."}, status=404)

    # Obtener los mensajes relacionados con la conversación
    mensajes = conversacion.mensajes.all()

    conversacion_serializada = {
        "id": conversacion.id,
        "usuario": conversacion.usuario.id,
        "titulo": conversacion.titulo,
        "fecha_creacion": conversacion.fecha_creacion.strftime("%d-%m-%Y %H:%M:%S"),
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

    return JsonResponse(conversacion_serializada, safe=False, status=200)


@csrf_exempt
def respuesta_chatbot(request):
    if request.method == "POST":
        try:
            # Obtener los datos enviados desde el frontend
            data = json.loads(request.body)

            mensaje = data.get("mensaje", "")
            id_conversacion = data.get("id_conversacion", "")
            titulo_conversacion = data.get("titulo_conversacion", "")
            fecha_creacion = data.get("fecha_creacion", "")

            

            print(data)

            respuesta_generada = "Esta es una respuesta generada por el chatbot"

            # Devolver la respuesta generada al frontend
            return JsonResponse(respuesta_generada, status=200, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)
