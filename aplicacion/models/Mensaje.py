from django.db import models
from .Usuario import Usuario

class Mensaje(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    remitente = models.CharField(max_length=10, choices=[('usuario', 'Usuario'), ('bot', 'Bot')], help_text="Quién envió el mensaje.")
    contenido = models.TextField(help_text="Contenido del mensaje.")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Hora en que se envió el mensaje.")
    contexto = models.JSONField(null=True, blank=True, help_text="Contexto adicional asociado al mensaje.")

    def __str__(self):
        return f"{self.remitente.capitalize()} - {self.timestamp}"