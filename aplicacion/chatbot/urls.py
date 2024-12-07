from django.urls import path, include

from aplicacion.chatbot import views

urlpatterns = [
    path('conversaciones/', views.listar_conversaciones),
    path('mensajes/', views.mensajes),
    path('respuesta-chatbot/', views.respuesta_chatbot),
    path('crear-conversacion/', views.nueva_conversacion),
]