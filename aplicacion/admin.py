from django.contrib import admin

from aplicacion.models import Usuario, Mensaje, Conversacion, RespuestaPredefinidas, DatosEjercicio

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Mensaje)
admin.site.register(Conversacion)
admin.site.register(RespuestaPredefinidas)
admin.site.register(DatosEjercicio)