from django.db import models

class RespuestaPredefinidas(models.Model):
    pregunta = models.CharField(max_length=255, unique=True, help_text="Pregunta frecuente.")
    respuesta = models.TextField(help_text="Respuesta predefinida para la pregunta.")
    categoria = models.CharField(max_length=50, null=True, blank=True, help_text="Categoría del tema.")

    def __str__(self):
        return f"{self.pregunta} - {self.categoria or 'General'}"