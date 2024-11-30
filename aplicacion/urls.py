from django.urls import path, include
from aplicacion import views

from aplicacion.chatbot import urls as chatbot_urls

urlpatterns = [
    
    path('chatbot/', include(chatbot_urls)),
    
    path('login/', views.login),
    path('logout/', views.logout_sesion),
]