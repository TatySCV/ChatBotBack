from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Campos adicionales
    bio = models.TextField(null=True, blank=True, help_text="Breve descripción del usuario.")
    preferencias = models.JSONField(null=True, blank=True, help_text="Preferencias específicas del usuario.")
    idioma = models.CharField(max_length=10, default='es', help_text="Idioma preferido del usuario.")
    es_activo_chatbot = models.BooleanField(default=True, help_text="Indica si el usuario está activo para el chatbot.")
    
    groups = models.ManyToManyField(Group, related_name='usuarios_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='usuarios_permissions', blank=True)

    def __str__(self):
        return self.username