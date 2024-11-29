from django.db import models
from .Usuario import Usuario
from .Mensaje import Mensaje

class Conversacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="conversaciones")
    titulo = models.CharField(max_length=255, default="Conversación sin título")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    mensajes = models.ManyToManyField(Mensaje, related_name="conversaciones")

    def __str__(self):
        return f"Conversación con {self.usuario.username} - {self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"